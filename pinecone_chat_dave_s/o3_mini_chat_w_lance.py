import os
import json
import re
import datetime
import pandas as pd
from time import time, sleep
from uuid import uuid4
import openai
import lancedb
import pyarrow as pa

MODEL                   = "gpt-4o-mini"
LANCE_DATABASE_ADDRESS  = "/home/adamsl/linuxBash/pinecone_chat_dave_s/lancedb"
OPENAI_API_KEY_FILE     = "/home/adamsl/key_openai.txt"
DATABASE_TABLE          = "youtube-chatbot"
PROMPT_TEMPLATE         = "/home/adamsl/linuxBash/agents/pinecone_chat_dave_s/prompt_response.txt"
NEXUS_ADDRESS           = "/home/adamsl/linuxBash/agents/nexus/"

# venv: source ../hp_agent_env/bin/activate
# ----- Helper Functions -----
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)

def save_json(filepath, payload):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Create directory path if it doesn't exist
    with open(filepath, 'w', encoding='utf-8') as outfile: # Write the JSON file with proper formatting
        json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=2)

def timestamp_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")

def gpt3_embedding(content, model='text-embedding-ada-002'):
    client = openai.OpenAI()  # Create a client instance
    response = client.embeddings.create(
        input=content,  # No need to wrap input in a list
        model=model
    )
    return response.data[0].embedding  # Accessing the new response structure

def ai_completion(prompt, model=MODEL, temp=0.0, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['USER:', 'RAVEN:']):
    client = openai.OpenAI()  # Create a client instance
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()  # Handle Unicode issues
    while retry < max_retry:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop
            )
            text = response.choices[0].message.content.strip()
            text = re.sub(r'[\r\n]+', '\n', text)
            text = re.sub(r'[\t ]+', ' ', text)
            filename = f'gpt3_logs/{int(time())}_gpt3.txt' # Logging response
            os.makedirs('gpt3_logs', exist_ok=True)
            save_file(filename, f"{prompt}\n\n==========\n\n{text}")
            return text
        except Exception as e:
            retry += 1
            print('Error communicating with OpenAI:', e)
            sleep(1)

    return f"GPT-3 error after {max_retry} retries: {e}"

def load_conversation(results_arg):
    """
    Expects results_arg to be a list of dictionaries with an 'id' key.
    Uses each id to load a JSON file from the local file system.
    """
    result = []
    for matching_unique in results_arg:
        filename = f"/home/adamsl/linuxBash/agents/nexus/{matching_unique['id']}.json"
        if not os.path.exists(filename):
            # print('file not found:', filename)
            continue

        info = load_json(filename)
        result.append(info)
    ordered = sorted(result, key=lambda d: d['time'], reverse=False)  # sort chronologically
    messages = [i['message'] for i in ordered]
    return '\n'.join(messages).strip()

# ----- Main Function using LanceDB -----
if __name__ == '__main__':
    convo_length = 30
    openai.api_key = open_file( OPENAI_API_KEY_FILE )
    db = lancedb.connect( LANCE_DATABASE_ADDRESS ) # Initialize LanceDB and define the schema
    schema = pa.schema([
        pa.field("id", pa.string()),
        pa.field("vector", pa.list_(pa.float32(), 1536)),  # Adjust 1536 to your vector dimension
        pa.field("speaker", pa.string()),
        pa.field("time", pa.float64()),
        pa.field("message", pa.string()),
        pa.field("timestring", pa.string())
    ])

    # Create or open the table with the defined schema
    if DATABASE_TABLE in db.table_names():
        tbl = db.open_table( DATABASE_TABLE )
    else:
        tbl = db.create_table( DATABASE_TABLE , schema=schema)

    first_time = True
    while True:
        data_for_lancedb_upsert = []
        if ( first_time ):    
            use_run_text = input("use linuxBash/agents/prompt.md? yes or <enter> ")
            if use_run_text.lower() == 'yes':
                user_input = open_file('/home/adamsl/linuxBash/agents/prompt.md')
                first_time = False
            else:
                user_input = input( f"\nmodel: { MODEL }  \nvector database: { LANCE_DATABASE_ADDRESS } database table: { DATABASE_TABLE } \n\nUSER: " )
                first_time = False
        else:
            user_input = input( f"\nmodel: { MODEL }  \nvector database: { LANCE_DATABASE_ADDRESS } database table: { DATABASE_TABLE } \n\nUSER: " )

        if user_input.lower() == 'quit' or user_input.lower() == 'exit' or user_input.lower() == 'x' or user_input.lower() == 'q':
            break

        timestamp_val = time()
        timestring = timestamp_to_datetime(timestamp_val)
        embedded_user_input = gpt3_embedding(user_input)
        unique_id = str(uuid4())
        metadata = {
            'id': unique_id,
            'vector': embedded_user_input,
            'speaker': 'USER',
            'time': timestamp_val,
            'message': user_input,
            'timestring': timestring
        }
        save_json(f"{ NEXUS_ADDRESS }{unique_id}.json", metadata)
        data_for_lancedb_upsert.append(metadata)

        # Querying LanceDB for relevant conversation history
        results_df = tbl.search(embedded_user_input, vector_column_name='vector').limit(convo_length).to_pandas()

        # Convert the results DataFrame into the format expected by load_conversation().
        if not results_df.empty and "id" in results_df.columns:
            matches = [{"id": uid} for uid in results_df["id"]]
            print( matches )
        else:
            matches = []
        conversation = load_conversation(matches)

        # Prepare the prompt using a template file.
        prompt_template = open_file( PROMPT_TEMPLATE )
        prompt = prompt_template.replace('<<CONVERSATION>>', conversation).replace('<<MESSAGE>>', user_input)

        # Get the AI's completion.
        ai_completion_text = ai_completion(prompt)

        # Save AI response to JSON and prepare for LanceDB upsert
        timestamp_val           = time()
        timestring              = timestamp_to_datetime(timestamp_val)
        embedded_ai_completion  = gpt3_embedding(ai_completion_text)
        unique_id               = str(uuid4())
        metadata                = {
            'id':           unique_id,
            'vector':       embedded_ai_completion,
            'speaker':      'RAVEN',
            'time':         timestamp_val,
            'message':      ai_completion_text,
            'timestring':   timestring
        }
        save_json(f"/home/adamsl/linuxBash/agents/nexus/{unique_id}.json", metadata)
        data_for_lancedb_upsert.append(metadata)

        # Upsert data into LanceDB
        df = pd.DataFrame(data_for_lancedb_upsert)
        tbl.add(df)

        print('\n\nRAVEN: %s' % ai_completion_text)
