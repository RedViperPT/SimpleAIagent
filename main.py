import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(sys.argv[1:])
    message = [
        types.Content(role="user", parts=[types.Part(text=user_prompt.replace('--verbose', '').strip())]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=message,
    )

    if len(sys.argv) < 2:
        print("Error: No prompt provided. Please provide a prompt as a command-line argument.")
        print("Usage: python main.py \"Your prompt here\"")
        sys.exit(1)
    
    if '--verbose' in user_prompt:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()