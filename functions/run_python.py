import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    abs_working_dir = os.path.realpath(working_directory)

    if not os.path.commonpath([full_path, abs_working_dir]) == abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            [sys.executable, file_path] + list(args),
            timeout=30,
            capture_output=True,
            text=True,  # text mode => stdout/stderr are str
            cwd=working_directory,
        )

        output_lines = []
        if completed_process.stdout:
            output_lines.append(f'STDOUT: {completed_process.stdout.strip()}')
        if completed_process.stderr:
            output_lines.append(f'STDERR: {completed_process.stderr.strip()}')
        if completed_process.returncode != 0:
            output_lines.append(f'Process exited with code {completed_process.returncode}')

        if not output_lines:
            return 'No output'

        return "\n".join(output_lines)
    except Exception as e:
        return f'Error: {e}'

schema_run_python = types.FunctionDeclaration(
    name="run_python",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING, description="Path to the Python file to execute, relative to the working directory."),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING, description="Optional arguments to pass to the Python file."),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
