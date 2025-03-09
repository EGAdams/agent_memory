# import modal
import os
import openai
from constants import DEFAULT_DIR, DEFAULT_MODEL, DEFAULT_MAX_TOKENS, EXTENSION_TO_SKIP
# import argparse
# from modal import stub

DEFAULT_DIR="/home/adamsl/linuxBash/pinecone_chat_dave_s/code_2_prompt/"
DEFAULT_MODEL="gpt-4o-mini"
DEFAULT_MAX_TOKENS="16000" # 128,000 tokens 16,384 tokens 

# stub = modal.Stub("smol-codetoprompt-v1")
# openai_image = modal.Image.debian_slim().pip_install("openai")

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def walk_directory(directory):
    code_contents = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not any(file.endswith(ext) for ext in EXTENSION_TO_SKIP):
                try:
                    relative_filepath = os.path.relpath(os.path.join(root, file), directory)
                    code_contents[relative_filepath] = read_file(os.path.join(root, file))
                except Exception as e:
                    code_contents[relative_filepath] = f"Error reading file {file}: {str(e)}"
    return code_contents


# @stub.local_entrypoint()
def main(prompt=None, directory=DEFAULT_DIR, model=DEFAULT_MODEL):
  code_contents = walk_directory(directory)

  # Now, `code_contents` is a dictionary that contains the content of all your non-image files
  # You can send this to OpenAI's text-davinci-003 for help

  context = "\n".join(f"{path}:\n{contents}" for path, contents in code_contents.items())
  system = "You are an AI debugger who is trying to fully describe a program, in order for another AI program to reconstruct every file, data structure, function and functionality. The user has provided you with the following files and their contents:"
  prompt = "My files are as follows: " + context + "\n\n" + (("Take special note of the following: " + prompt) if prompt else "")
  prompt += "\n\nDescribe the program in markdown using specific language that will help another AI program reconstruct the given program in as high fidelity as possible."
  
  res = generate_response(system, prompt, model)
  # print res in teal
  print("\033[96m" + res + "\033[0m")


# @stub.function(
#     image=openai_image,
#     secret=modal.Secret.from_dotenv(),
#     retries=modal.Retries(
#         max_retries=3,
#         backoff_coefficient=2.0,
#         initial_delay=1.0,
#     ),
#     concurrency_limit=5,
#     timeout=120,
# )
def generate_response(system_prompt, user_prompt, model=DEFAULT_MODEL, *args):
    openai.api_key = os.environ["OPENAI_API_KEY"] # Set up your OpenAI API credentials
    messages = []
    messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    # loop thru each arg and add it to messages alternating role between "assistant" and "user"
    role = "assistant"
    for value in args:
        messages.append({"role": role, "content": value})
        role = "user" if role == "assistant" else "assistant"

    params = {
        'model': model,
        "messages": messages,
        "max_tokens": DEFAULT_MAX_TOKENS, # 8000, #16400, #2500,
        "temperature": 0,
    }
    
    response = openai.ChatCompletion.create(**params) # Send the API request
    reply = response.choices[0]["message"]["content"] # Get the reply from the API response
    return reply

if __name__ == "__main__":
    main()