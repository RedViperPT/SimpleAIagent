import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python 
from functions.write_file import schema_write_file
from functions.call_functions import call_function


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
When asked to run a Python file and no arguments are provided, run it with no arguments.
"""

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python,
            schema_write_file,
        ]
    )

    if len(sys.argv) < 2:
        print("Error: No prompt provided. Please provide a prompt as a command-line argument.")
        print("Usage: python main.py \"Your prompt here\"")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    verbose = "--verbose" in user_prompt

    message = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt.replace("--verbose", "").strip())],
        ),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=message,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        print(response.text)
        return

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose=verbose)

        if not function_call_result.parts or not hasattr(
            function_call_result.parts[0], "function_response"
        ):
            raise RuntimeError("Fatal: no function_response in call_function result")

        response_dict = function_call_result.parts[0].function_response.response

        print("Response:")
        print(response_dict.get("result") or response_dict.get("error"))

if __name__ == "__main__":
    main()
