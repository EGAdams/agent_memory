from uuid import uuid4
import os, time, datetime
import openai
import sys

# Constants
HOME_DIR         = os.path.expanduser( "~" )
sys.path.append( f"{ HOME_DIR }/agent_memory/embedding_tools" )
from extract_store_embeddings import EmbeddingGenerator, LanceDBManager, NexusStorage

MODEL = "gpt-4o-mini"

# Constants
LANCEDB_TABLE_NAME = "the-factory-storage"
PROMPT_ROOT      = f"{ HOME_DIR }/agent_memory/embedding_tools"
STORAGE_PATH     = f"{ HOME_DIR }/agent_memory/embedding_tools/{ LANCEDB_TABLE_NAME }"
NEXUS_DIR        = f"{ STORAGE_PATH }/nexus" # Local storage for complete code snippets
DATABASE_DIR     = f"{ STORAGE_PATH }/vector_database"

CONTEXT = """
# Persona
Expert TypeScript developer and seasoned user of GoF Design Patterns.

# Context
You are an AI that helps the user understand and modify code if needed.

# Instructions
You have been given relevant source code to answer questions, create additional code, or perform modifications.
"""
MAX_SNIPPET_MATCHES = 40

def ai_completion( prompt, model = MODEL, temp = 0.0, top_p = 1.0, tokens = 8000,
                  freq_pen = 0.0, pres_pen = 0.0 ):
    """
    Call OpenAI ChatCompletion with a system+user prompt structure.
    Returns the text of the first response choice.
    """
    api_key_path = f"{ HOME_DIR }/linuxBash/key_openai.txt"
    api_key_arg = EmbeddingGenerator.load_api_key( api_key_path )
    client = openai.OpenAI( api_key = api_key_arg )

    messages = [
        { "role": "system", "content": CONTEXT },
        { "role": "user", "content": prompt }
    ]

    try:
        response = client.chat.completions.create(
            model = model,
            messages = messages,
            temperature = temp,
            max_tokens = tokens,
            top_p = top_p,
            frequency_penalty = freq_pen,
            presence_penalty = pres_pen
        )
        return response.choices[ 0 ].message.content
    except Exception as e:
        return f"GPT-4 error: { e }"


def open_file( filepath ):
    """Open a text file and return its contents."""
    with open( filepath, 'r', encoding = 'utf-8' ) as infile:
        return infile.read()


class CodeQueryProcessor:
    """Handles querying the codebase, retrieving relevant code, and generating modifications."""

    def __init__( self, db_manager, embedding_generator, nexus_storage ):
        self.db_manager = db_manager
        self.embedding_generator = embedding_generator
        self.nexus_storage = nexus_storage

    def process_user_request( self, user_request ):
        """Processes a user request, retrieves relevant code, and generates AI modifications."""
        user_request = user_request.strip()
        if not user_request:
            print( "Empty input. Try again." )
            return

        # Generate user embedding
        embedded_request = self.embedding_generator.generate_embedding( user_request )

        # Retrieve relevant code snippets from LanceDB
        matching_ids = self.db_manager.search_embeddings( embedded_request, top_k = MAX_SNIPPET_MATCHES )
        retrieved_code = self.load_code_snippets( matching_ids )

        # Construct AI prompt
        prompt_template = "# User Request:\n<<REQUEST>>\n# Relevant Code:\n<<CODE>>"
        prompt_text = prompt_template.replace( "<<REQUEST>>", user_request ).replace( "<<CODE>>", retrieved_code )

        # save prompt to file with a unique filename that has a timestamp
        timestamp_val = time.strftime("mon_%b_%d__%I_%M_%p_%Ss", time.localtime())
        with open( f"{ HOME_DIR }/agent_memory/embedding_tools/prompts/ai_code_prompt_{ timestamp_val }.md", "w" ) as file:
            file.write( prompt_text )

        # Generate AI response
        ai_text = ai_completion( prompt_text )

        # Save AI-generated response
        timestamp_val = time.strftime("mon_%b_%d__%I_%M_%p_%Ss", time.localtime())
        with open( f"{ HOME_DIR }/agent_memory/embedding_tools/responses/ai_code_response_{ timestamp_val }.md", "w" ) as file:
            file.write( ai_text )

        print( "\n\nAI Response:" )
        print( ai_text )

    def load_code_snippets(self, matching_ids):
        """Loads relevant code snippets from the Nexus storage."""
        snippets = []
        for match_id in matching_ids:
            code = self.nexus_storage.get_function(match_id)
            if code:
                snippets.append(f"```typescript\n{code}\n```")

        if not snippets:
            sys.exit("*** ERROR: No relevant code found. ***")
            # if there was no relevant code in the storage, 
            # we would not be using this tool!

        return "\n".join(snippets)


# Initialize components
embedding_generator = EmbeddingGenerator()
nexus_storage = NexusStorage( NEXUS_DIR )
db_manager = LanceDBManager( DATABASE_DIR, LANCEDB_TABLE_NAME )
pipeline = CodeQueryProcessor( db_manager, embedding_generator, nexus_storage )

# User input loop
first_time = True
while True:
    data_for_lancedb_upsert = []
    if ( first_time ):    
        use_run_text = input( f"use { PROMPT_ROOT }/prompt.md? yes or <enter> " )
        if use_run_text.lower() == 'yes':
            user_input = open_file( f"{ PROMPT_ROOT }/prompt.md" )
            first_time = False
        else:
            user_input = input( f"\nmodel: { MODEL }  \nvector database: { DATABASE_DIR } \ndatabase table: { LANCEDB_TABLE_NAME }\nmax snippet matches: { MAX_SNIPPET_MATCHES } \n\nUSER: " )
            first_time = False
    else:
        user_input = input( f"\nmodel: { MODEL }  \nvector database: { DATABASE_DIR } \ndatabase table: { LANCEDB_TABLE_NAME }\nmax snippet matches: { MAX_SNIPPET_MATCHES } \n\nUSER: " )

    if user_input.lower() == 'quit' or user_input.lower() == 'exit' or user_input.lower() == 'x' or user_input.lower() == 'q':
        break
    # user_input = """
       
    #     """

    pipeline.process_user_request( user_input )
