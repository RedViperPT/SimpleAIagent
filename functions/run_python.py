import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
        
    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    abs_working_dir = os.path.realpath(working_directory)

    if not os.path.commonpath([full_path, abs_working_dir]) == abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if full_path[-3:] != '.py':
        # print(f'{full_path[-3:]}')
        return f'Error: "{file_path}" is not a Python file.'


    try:
        completed_process = subprocess.run(['python', file_path] + args, timeout=30, capture_output=True, cwd=working_directory,)
        
        output = []
        if completed_process.stdout:
            output.append(f'STDOUT: {completed_process.stdout.decode().strip()}')
        if completed_process.stderr:
            output.append(f'STDERR: {completed_process.stderr.decode().strip()}')
        if completed_process.returncode != 0:
            output.append(f'Process exited with code {completed_process.returncode}')
        if not output:
            return f"Error: executing Python file: {e}"
        return "\n".join(output)

    except Exception as e:
        return f'Error: {e}'
