import os

def write_file(working_directory, file_path, content):
    
    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    abs_working_dir = os.path.realpath(working_directory)

    if not os.path.commonpath([full_path, abs_working_dir]) == abs_working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        try:
            os.makedirs(os.path.dirname(full_path))
        except Exception as e:
            return f"Error: Creating directory: {e}"
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Writing file: {e}"