# https://chatgpt.com/share/67bb27f9-df48-8006-8923-89b42e2933dd
import os
import json
import datetime

from uuid import uuid4
from time import time
import openai
import tempfile
import shutil
import json
import requests
from code_parser.code_parser            import CodeParser
from lance_db_manager.lance_db_manager  import LanceDBManager

def get_java_types():

    # URL of the node-types.json file in the tree-sitter-java repository
    url = "https://raw.githubusercontent.com/tree-sitter/tree-sitter-java/master/src/node-types.json"

    # Fetch the JSON data
    response = requests.get(url)
    node_types_data = response.json()

    # Extract the 'type' field from each node and add to a set
    java_types = {node['type'] for node in node_types_data}

    # Display the set of Java node types
    # print( f"Java node types: {java_types}")
    return java_types

# CACHED_EMBEDDINGS_PATH  = os.path.join( "cached_embeddings.json" ) # not sure why we need this yet.
                                                                    # it was in some original that I
                                                                    # copied.
# it was also mentioned in the
# Project Specific Constants
ANDROID_BASE        = "/home/adamsl/AndroidBase"
CODE_ROOT           = f"{ ANDROID_BASE }/MCBACore/src/main/java/com/awm/mcba/base"
STORAGE_PATH        = f"{ ANDROID_BASE }/embedding_tools/storage"

# Universal Constants
NEXUS_DIR           = f"{ STORAGE_PATH }/nexus"                  
DATABASE_DIR        = f"{ STORAGE_PATH }/vector_database"
EMBEDDINGS_MODEL    = "text-embedding-ada-002"

class StorageManager:
    """Handles coordinated deletion and modification of Nexus files and LanceDB vector database entries."""

    def __init__(self, nexus_storage, db_manager, embedding_generator):
        self.nexus_storage = nexus_storage
        self.db_manager = db_manager
        self.embedding_generator = embedding_generator

    def delete_entry(self, unique_id):
        """Delete a Nexus file and its corresponding entry in LanceDB."""
        file_deleted = self.nexus_storage.delete_function(unique_id)
        db_deleted = self.db_manager.delete_entry(unique_id)

        if file_deleted and db_deleted:
            print(f"✅ Successfully deleted {unique_id} from both Nexus and LanceDB.")
        elif file_deleted:
            print(f"⚠️ Deleted Nexus file for {unique_id}, but entry may still exist in LanceDB.")
        elif db_deleted:
            print(f"⚠️ Deleted LanceDB entry for {unique_id}, but Nexus file may still exist.")
        else:
            print(f"❌ Failed to delete {unique_id}. Entry may not exist in either Nexus or LanceDB.")

    def modify_entry(self, unique_id, new_function_code, is_valid_java=True):
        """Modify an existing function by replacing its Nexus file and embedding."""
        print(f"🔄 Modifying function {unique_id}...")

        # Step 1: Delete the old entry
        self.delete_entry(unique_id)

        # Step 2: Generate new embedding
        new_embedding = self.embedding_generator.generate_embedding(new_function_code)

        # Step 3: Save the new function in Nexus
        new_nexus_path = self.nexus_storage.save_function(new_function_code, unique_id, is_valid_java)

        # Step 4: Insert new function into LanceDB
        timestamp_val = time.time()
        new_metadata = {
            "id": unique_id,
            "vector": new_embedding,
            "filepath": new_nexus_path,
            "time": timestamp_val,
            "nexus_path": new_nexus_path
        }
        self.db_manager.store_embeddings([new_metadata])

        print(f"✅ Function {unique_id} successfully updated in both Nexus and LanceDB.")

class FileProcessor:
    """Handles reading files and extracting functions."""

    def __init__(self, directory, language_arg="java" ):
        self.directory = directory
        self.file_extension = f".{ language_arg }" # prepend dot for file extension
        self.code_parser = CodeParser( language_arg )
        self.types = get_java_types()

    def get_files(self):
        """Retrieve all java files from the directory."""
        debug_info = []
        result = []
        print(f"Processing files in {self.directory}..." )
        for root, _, files in os.walk(self.directory):
            debug_info.append(f"Checking directory: {root}, Files: {files}")
            for file in files:
                if file.endswith(self.file_extension):
                    full_path = os.path.join(root, file)
                    debug_info.append(f"Matched file: {full_path}")
                    result.append(full_path)
        
        print("\n".join(debug_info))  # Print all debug info at once
        return result

    def get_tree_sitter_functions(self, filepath):
        """Extract method and class definitions from a Java file using Tree-Sitter."""
        if "node_modules" in filepath.split(os.sep):
            print(f"Skipping file in node_modules: {filepath}")
            return []

        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read().replace("\r", "\n")

        tree = self.code_parser.parser.parse(bytes(code, "utf8"))
        root = tree.root_node
        functions = []

        def extract_functions(node):
            if node.type in {"method_declaration", "class_declaration"}:
                code_segment = code[node.start_byte:node.end_byte]
                functions.append({"code": code_segment, "filepath": filepath})
            for child in node.children:
                extract_functions(child)

        extract_functions(root)
        return functions

class EmbeddingGenerator:
    """Generates embeddings using OpenAI's API."""

    def __init__(self, model=EMBEDDINGS_MODEL, api_key_path="~/linuxBash/key_openai.txt" ):
        self.model = model
        self.openai = openai
        self.openai.api_key = self.load_api_key(api_key_path)

    @staticmethod
    def load_api_key(filepath):
        """Load the OpenAI API key from a file."""
        with open(os.path.expanduser(filepath), "r" ) as f:
            return f.read().strip()

    def generate_embedding(self, content):
        """Generate embedding vector for a given code snippet."""
        print( f"Generating embedding for: { content }")
        content = content.encode("ASCII", errors="ignore" ).decode()
        response = self.openai.OpenAI().embeddings.create(input=[content], model=self.model)
        return response.data[0].embedding

class NexusStorage:
    """Handles storing and retrieving java functions locally."""

    def __init__(self, nexus_dir=NEXUS_DIR):
        self.nexus_dir = nexus_dir
        os.makedirs(nexus_dir, exist_ok=True)

    def save_function(self, function_code, unique_id, is_valid_java=True):
        """Store the original java function in a file under Nexus safely."""
        extension = "java" if is_valid_java else "txt"
        file_path = os.path.join(self.nexus_dir, f"{unique_id}.{extension}")

        # Write to a temp file first, then move to final destination
        temp_file = tempfile.NamedTemporaryFile(delete=False, dir=self.nexus_dir, suffix=f".{extension}")

        try:
            with open(temp_file.name, "w", encoding="utf-8") as f:
                f.write(function_code)
            shutil.move(temp_file.name, file_path)  # Atomic move
        finally:
            if os.path.exists(temp_file.name):  # Cleanup if failed
                os.remove(temp_file.name)

        return file_path

    def get_function(self, unique_id):
        """Retrieve a function by ID from Nexus storage safely."""
        for ext in ["java", "txt"]:  # Check both possible extensions
            file_path = os.path.join(self.nexus_dir, f"{unique_id}.{ext}")
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        return f.read()
                except Exception as e:
                    print(f"Error reading function file {file_path}: {e}")
                    return None

        print(f"Function {unique_id} not found in Nexus storage.")
        return None
    
    def delete_function(self, unique_id):
        """Delete a function file from Nexus storage."""
        for ext in ["java", "txt"]:  # Check both possible extensions
            file_path = os.path.join(self.nexus_dir, f"{unique_id}.{ext}")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted Nexus file: {file_path}")
                    return True
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
                    return False
        print(f"Nexus file for {unique_id} not found.")
        return False

class CodeEmbeddingPipeline:
    """Orchestrates the entire embedding process."""

    def __init__(self, code_root):
        self.file_processor         = FileProcessor(code_root)
        self.embedding_generator    = EmbeddingGenerator()
        self.nexus_storage          = NexusStorage()
        self.db_manager             = LanceDBManager( DATABASE_DIR, "android_base" )

    def process_codebase( self ):
        """Extracts functions, generates embeddings, and stores results."""
        all_files = self.file_processor.get_files() # <---------------------- entry point -----------------------------<<
        print(f"Processing {len(all_files)} java files..." )

        all_data = []
        for file in all_files:
            functions = self.file_processor.get_tree_sitter_functions(file)
            for func in functions:
                embedding = self.embedding_generator.generate_embedding(func["code"])
                unique_id = str(uuid4())
                timestamp_val = time()   # TODO: store time of file modification AND
                                         #       the time that this embedding was generated?
                # Save the original function to Nexus
                nexus_path = self.nexus_storage.save_function(func["code"], unique_id)

                # Store only the embedding and path reference in LanceDB
                metadata = {                    # TODO: store class name?
                    "id": unique_id,
                    "vector": embedding,
                    "filepath": func["filepath"],
                    "time": timestamp_val,
                    "nexus_path": nexus_path    # Store the Nexus path to 
                }                               # reconstruct the entire function later.

                all_data.append(metadata)

        if all_data:
            self.db_manager.store_embeddings(all_data)
            print("Embeddings stored successfully in LanceDB." )

    def search_code(self, query):
        """Perform a vector search and retrieve matching java functions."""
        query_embedding = self.embedding_generator.generate_embedding(query)
        matching_ids = self.db_manager.search_embeddings(query_embedding)

        if not matching_ids:
            print("No matches found." )
            return

        print("\nMatching java functions:\n" )
        for match_id in matching_ids:
            function_code = self.nexus_storage.get_function(match_id)
            if function_code:
                print(f"Function ID: {match_id}" )
                print(function_code)
                print("\n" + "=" * 50 + "\n" )

if __name__ == "__main__":
    pipeline = CodeEmbeddingPipeline(CODE_ROOT)
    pipeline.process_codebase()
