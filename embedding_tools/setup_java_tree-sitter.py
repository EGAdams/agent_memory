import os
import subprocess
from tree_sitter import Language, Parser

# Set up paths
BASE_DIR = os.path.expanduser("~/tree_sitter_languages")
JAVA_REPO = os.path.join(BASE_DIR, "tree-sitter-java")
BUILD_DIR = os.path.join(BASE_DIR, "build")
LIBRARY_PATH = os.path.join(BUILD_DIR, "my-languages.so")

# Ensure the build directory exists
os.makedirs(BUILD_DIR, exist_ok=True)

# Clone the Java grammar repo if it's not already cloned
if not os.path.exists(JAVA_REPO):
    print("Cloning tree-sitter-java repository...")
    subprocess.run(["git", "clone", "https://github.com/tree-sitter/tree-sitter-java.git", JAVA_REPO], check=True)

# Build the shared library with the correct API
print("Building Java Tree-sitter parser manually...")
Language.build_library(
    LIBRARY_PATH,
    [JAVA_REPO]
)

# Load the Java language using the correct API
print("Loading Java parser...")
java_language = Language(LIBRARY_PATH, 'java')


# Create and configure the parser
java_parser = Parser()
java_parser.set_language(java_language)

print("✅ Java Tree-sitter setup completed successfully!")
