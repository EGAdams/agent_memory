def get_file_extension(language_name):
    # Mapping of language names to their file extensions
    language_extensions = {
        "java": ".java",
        "typescript": ".ts",
        "javascript": ".js",
        "python": ".py",
        "ruby": ".rb",
        "csharp": ".cs",
        "c++": ".cpp",
        "c": ".c",
        "go": ".go",
        "swift": ".swift",
        "kotlin": ".kt",
        "php": ".php",
        "perl": ".pl",
        "r": ".r",
        "scala": ".scala",
        "haskell": ".hs",
        "lua": ".lua",
        "rust": ".rs",
        "dart": ".dart",
        "elixir": ".ex",
        "erlang": ".erl",
        "objective-c": ".m",
        "shell": ".sh",
        "powershell": ".ps1",
        "vbscript": ".vbs",
        "typescriptreact": ".tsx",  # For TSX files
        "jsx": ".jsx",  # For JSX files
        # Add more languages and their extensions as needed
    }

    # Normalize the language name to lowercase to ensure case-insensitive matching
    normalized_language_name = language_name.lower()

    # Retrieve the file extension from the dictionary
    return language_extensions.get(normalized_language_name, None)

# Example usage
language_name = "TypeScript"
extension = get_file_extension(language_name)
if extension:
    print(f"The file extension for {language_name} is {extension}")
else:
    print(f"No file extension found for {language_name}")
