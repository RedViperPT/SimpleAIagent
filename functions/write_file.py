import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    abs_working_dir = os.path.realpath(working_directory)

    if os.path.commonpath([full_path, abs_working_dir]) != abs_working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        parent_dir = os.path.dirname(full_path) or abs_working_dir
        os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        return f"Error: Creating directory: {e}"

    if os.path.isdir(full_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Writing file: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the specified file path. Creates a file if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to write the file to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)
