from uuid import uuid4
import os, time, datetime
import openai

import sys
# Constants
HOME_DIR         = os.path.expanduser( "~" )
sys.path.append( f"{ HOME_DIR }/monitored-objects/embedding_tools" )
from extract_store_embeddings import EmbeddingGenerator, LanceDBManager, NexusStorage

MODEL = "gpt-4o-mini"

# Constants
PROMPT_ROOT      = f"{ HOME_DIR }/monitored-objects/embedding_tools"
STORAGE_PATH     = f"{ HOME_DIR }/monitored-objects/embedding_tools/storage"
NEXUS_DIR        = f"{ STORAGE_PATH }/nexus"                         # Local storage for TypeScript files
DATABASE_DIR     = f"{ STORAGE_PATH }/vector_database"
LANCEDB_TABLE_NAME = "android_base"

def ai_completion(prompt, model=MODEL, temp=0.0, top_p=1.0, tokens=8000,
                  freq_pen=0.0, pres_pen=0.0):
    """
    Call OpenAI ChatCompletion with a system+user prompt structure.
    Returns the text of the first response choice.
    """
    api_key_path=f"{ HOME_DIR}/linuxBash/key_openai.txt"
    api_key_arg = EmbeddingGenerator.load_api_key(api_key_path)
    client = openai.OpenAI(api_key=api_key_arg)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temp,
            max_tokens=tokens,
            top_p=top_p,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"GPT-3 error: {e}"

def timestamp_to_datetime(unix_time):
    """Convert a Unix timestamp to a human-readable datetime string."""
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")

def open_file(filepath):
    """Open a text file and return its contents."""
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
class ConversationProcessor:
    """Handles user input, AI response generation, and embedding storage."""

    def __init__(self, db_manager, embedding_generator, nexus_storage, convo_length=5):
        self.db_manager = db_manager
        self.embedding_generator = embedding_generator
        self.nexus_storage = nexus_storage
        self.convo_length = convo_length

    def process_user_input(self, user_input):
        """Processes user input, generates an AI response, and stores both."""
        user_input = user_input.strip()
        if not user_input:
            print("Empty input. Try again.")
            return

        data_for_lancedb_upsert = []
        timestamp_val = time.time()

        # Generate user embedding
        embedded_user_input = self.embedding_generator.generate_embedding(user_input)
        unique_id = str(uuid4())

        # Store user input in Nexus
        user_nexus_path = self.nexus_storage.save_function(user_input, unique_id, is_valid_typescript=False)

        # Prepare metadata for LanceDB
        user_metadata = {
            "id": unique_id,
            "vector": embedded_user_input,
            "filepath": user_nexus_path,  # Using the Nexus path as the file reference
            "time": timestamp_val,
            "nexus_path": user_nexus_path
        }
        data_for_lancedb_upsert.append(user_metadata)

        # Retrieve conversation history from LanceDB
        matching_ids = self.db_manager.search_embeddings(embedded_user_input, self.convo_length)
        conversation = self.load_conversation(matching_ids)

        # Build AI response prompt
        prompt_template = open_file(f"{HOME_DIR}/monitored-objects/embedding_tools/prompt_response.txt")
        prompt_text = prompt_template.replace("<<CONVERSATION>>", conversation).replace("<<MESSAGE>>", user_input)

        # Generate AI response
        ai_text = ai_completion(prompt_text)

        # Generate AI embedding
        timestamp_val = time.time()
        embedded_ai_completion = self.embedding_generator.generate_embedding(ai_text)
        unique_id = str(uuid4())

        # Store AI response in Nexus
        ai_nexus_path = self.nexus_storage.save_function(ai_text, unique_id, is_valid_typescript=False)

        # Prepare metadata for LanceDB
        ai_metadata = {
            "id": unique_id,
            "vector": embedded_ai_completion,
            "filepath": ai_nexus_path,  # Using the Nexus path as the file reference
            "time": timestamp_val,
            "nexus_path": ai_nexus_path
        }
        data_for_lancedb_upsert.append(ai_metadata)

        # Store embeddings in LanceDB
        if data_for_lancedb_upsert:
            self.db_manager.store_embeddings(data_for_lancedb_upsert)

        print("\n\nRAVEN:", ai_text)
        # write ai_text to an .md file using "ai_answer_{ Unix_time }.md"
        with open(f"{HOME_DIR}/monitored-objects/ai_answer_{timestamp_val}.md", "w") as file:
            file.write(ai_text)
        

    def load_conversation(self, matching_ids):
        """Loads past conversation messages from stored Nexus files."""
        conversation = []
        for match_id in matching_ids:
            message = self.nexus_storage.get_function(match_id)
            if message:
                conversation.append(message)
        return "\n".join(conversation) if conversation else "No previous conversation found."


# Example usage:
embedding_generator = EmbeddingGenerator()
nexus_storage       = NexusStorage()
db_manager          = LanceDBManager()
pipeline            = ConversationProcessor(db_manager, embedding_generator, nexus_storage)
# user_input          = input("\n\nUSER: ")
first_time = True
while True:
    data_for_lancedb_upsert = []
    if ( first_time ):    
        use_run_text = input("use linuxBash/agents/prompt.md? yes or <enter> ")
        if use_run_text.lower() == 'yes':
            user_input = open_file( f"{ PROMPT_ROOT }/prompt.md " )
            first_time = False
        else:
            user_input = input( f"\nmodel: { MODEL }  \nvector database: { DATABASE_DIR } \ndatabase table: { LANCEDB_TABLE_NAME } \n\nUSER: " )
            first_time = False
    else:
        user_input = input( f"\nmodel: { MODEL }  \nvector database: { DATABASE_DIR } \ndatabase table: { LANCEDB_TABLE_NAME } \n\nUSER: " )

    if user_input.lower() == 'quit' or user_input.lower() == 'exit' or user_input.lower() == 'x' or user_input.lower() == 'q':
        break

    pipeline.process_user_input( user_input )
