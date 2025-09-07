import os
from google.genai import types
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):

    full_path = os.path.realpath(os.path.join(working_directory, file_path))                             
    abs_working_dir = os.path.realpath(working_directory)

    if not os.path.commonpath([full_path, abs_working_dir]) == abs_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            file_content = f.read(MAX_CHARS)
            if os.path.getsize(full_path) > MAX_CHARS:
                file_content += f'[...File "{file_path}" truncated at "{MAX_CHARS}"characters]'
                return file_content
            else:
                return file_content
    except Exception as e:
        return f"Error: Reading file: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)