import os
import ctypes
from tree_sitter import Language, Parser

# Option 2: Create a Parser and then set its language property.
# parser = Parser()
# parser.language = java_language

# Now parse some code.
# source_code = b'public class Test { }'
# tree = parser.parse(source_code)
# print( tree.root_node.type)

class CodeParser:
    def __init__(self, language: str):
        self.parser = Parser()
        tree_sitter_lib_so = f"/home/adamsl/AndroidBase/embedding_tools/tree-sitter-{ language }/libtree-sitter-{ language }.so"
        
        # Load the shared library using ctypes.
        lib = ctypes.CDLL( tree_sitter_lib_so )
        # Ensure the function returns an unsigned pointer.
        lib.tree_sitter_java.restype = ctypes.c_void_p
        lang_ptr = lib.tree_sitter_java()

        # Create the Language object using the pointer.
        java_language = Language(lang_ptr)

        # Option 1: Pass the language when instantiating Parser.
        parser = Parser(java_language)
        if not os.path.exists( tree_sitter_lib_so ): # *** ERROR if .so file is not found
            raise FileNotFoundError( f"Tree-sitter library for { language } not found at { tree_sitter_lib_so }" )
        self.parser = parser

    def extract_nodes(self, node, code):
        nodes = []
        if node.type == 'class_specifier':
            # Extract the class
            nodes.append((node.start_point, node.end_point, code[node.start_byte:node.end_byte]))
            print(f"Extracted class node from line {node.start_point[0] + 1} to {node.end_point[0] + 1}:\n{code[node.start_byte:node.end_byte]}")
        elif node.type == 'function_definition':
            # Extract the function only if it's not a method of a class
            if node.parent and node.parent.type != 'class_specifier':
                nodes.append((node.start_point, node.end_point, code[node.start_byte:node.end_byte]))
                print(f"Extracted function node from line {node.start_point[0] + 1} to {node.end_point[0] + 1}:\n{code[node.start_byte:node.end_byte]}")
        
        # Recursively extract nodes from the children
        for child in node.children:
            nodes.extend(self.extract_nodes(child, code))

        return nodes

    def parse_file(self, file_path: str):
        with open(file_path, 'r') as file:
            code = file.read()

        print(f"\nParsing file: {file_path}")
        tree = self.parser.parse(bytes(code, 'utf8'))
        nodes = self.extract_nodes(tree.root_node, code)
        
        # Convert the nodes to the desired output format
        output = []
        for start_point, end_point, node_code in nodes:
            line_coverage = (start_point[0] + 1, end_point[0] + 1)  # Tree-sitter uses 0-indexed line numbers
            output.append((file_path, line_coverage, node_code))

        print(f"Finished parsing file: {file_path}")
        return output

    def parse_directory(self, directory_path: str):
        parsed_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(self.language.file_extension):
                    file_path = os.path.join(root, file)
                    parsed_files.extend(self.parse_file(file_path))
        return parsed_files

# Create a CodeParser instance for testing
# code_parser = CodeParser('cpp')
# The code_parser.parse_file method expects a real file path. We need 
# a real file path to a C++ file to test it.
# code_parser.parse_file( "./tennis-game/SetDrawer/SetDrawer.h" )