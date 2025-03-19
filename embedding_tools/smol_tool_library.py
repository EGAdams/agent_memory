import os, sys
import subprocess
from smolagents import CodeAgent, LiteLLMModel, tool
import openai

# Constants
# HOME_DIR         = os.path.expanduser( "~" )
# sys.path.append( f"{ HOME_DIR }/agent_memory/embedding_tools" )

# # Set your OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Initialize the LiteLLMModel with gpt-4o-mini
# model = LiteLLMModel(
#     model_id="gpt-4o-mini",
#     api_key=openai.api_key,
#     temperature=0.2,
#     max_tokens=8000
# )

@tool
def read_file(file_path: str) -> str:
    """
    Reads the content of the specified file.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file, or an error message if reading fails.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return str(e)


@tool
def write_file(file_path: str, content: str) -> str:
    """
    Writes content to the specified file.

    Args:
        file_path (str): The path to the file to be written to.
        content (str): The content to write to the file.

    Returns:
        str: A confirmation message if successful, or an error message if writing fails.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Content written to: {file_path}"
    except Exception as e:
        return str(e)

@tool
def delete_file(file_path: str) -> str:
    """
    Deletes the specified file.

    Args:
        file_path (str): The path to the file to be deleted.

    Returns:
        str: A confirmation message if successful, or an error message if deletion fails.
    """
    try:
        os.remove(file_path)
        return f"File deleted: {file_path}"
    except Exception as e:
        return str(e)

@tool
def replace_code_block(file_path: str, old_code_start: str, old_code_end: str, new_code: str) -> str:
    """
    Replaces a block of code in a file using sed. Works with TypeScript, JavaScript, Java, Python, and C++.

    Args:
        file_path (str): The path to the file to modify.
        old_code_start (str): The first line of the code block to replace.
        old_code_end (str): The last line of the code block to replace.
        new_code (str): The replacement code.

    Returns:
        str: A confirmation message if successful, or an error message if the sed command fails.
    """
    try:
        # Escape characters for sed replacement
        new_code_sed = new_code.replace("/", "\\/").replace("&", "\\&").replace("\n", "\\n")

        # Construct the sed command to replace the multi-line block
        sed_command = f'/^{old_code_start}/,/{old_code_end}/c\\{new_code_sed}'

        # Execute the sed command
        subprocess.run(['sed', '-i', sed_command, file_path], check=True, capture_output=True, text=True)

        return f"Successfully replaced code block in: {file_path}"
    except subprocess.CalledProcessError as e:
        return f"Sed command failed: {e.stderr}"
    except Exception as e:
        return str(e)



# Define tools for directory management
@tool
def list_directory_contents(path: str) -> str:
    """
    Lists contents of the specified directory.

    Args:
        path (str): The path to the directory whose contents are to be listed.

    Returns:
        str: A newline-separated string of directory contents, or an error message if listing fails.
    """
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        return str(e)

@tool
def create_directory(path: str) -> str:
    """
    Creates a new directory at the specified path.

    Args:
        path (str): The path where the new directory will be created.

    Returns:
        str: A confirmation message if successful, or an error message if creation fails.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return f"Directory created at: {path}"
    except Exception as e:
        return str(e)

@tool
def delete_directory(path: str) -> str:
    """
    Deletes the specified directory.

    Args:
        path (str): The path to the directory to be deleted.

    Returns:
        str: A confirmation message if successful, or an error message if deletion fails.
    """
    try:
        os.rmdir(path)
        return f"Directory deleted: {path}"
    except Exception as e:
        return str(e)
    
@tool
def get_current_directory() -> str:
    """
    Retrieves the current working directory.

    Args:
        None

    Returns:
        str: The absolute path of the current working directory.
    """
    try:
        return os.getcwd()
    except Exception as e:
        return str(e)


# Initialize the CodeAgent with the model and tools
# agent = CodeAgent(
#     tools=[
#         list_directory_contents,
#         create_directory,
#         delete_directory,
#         read_file,
#         write_file,
#         delete_file,
#         modify_file_with_sed
#     ],
#     model=model
# )

# Example: Generate Python code to list files in a directory
# task = """
# """
# response = agent.run(task)
# print(response)
