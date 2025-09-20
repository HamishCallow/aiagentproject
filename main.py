import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) < 2:
        print("error: no prompt given"); sys.exit(1)

    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info]
    )

    response = client.models.generate_content(
        model="gemini-1.5-flash-002",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if response.function_calls:
        for fc in response.function_calls:
            print(f"Calling function: {fc.name}({fc.args})")
    else:
        print(response.text or "[no text returned]")

    verbose = ("--verbose" in sys.argv[2:])
    um = response.usage_metadata

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {um.prompt_token_count}")
        print(f"Response tokens: {um.candidates_token_count}")

    if response.candidates:
        fr = response.candidates[0].finish_reason
        print(f"Finish reason: {fr}")

if __name__ == "__main__":
    main()
