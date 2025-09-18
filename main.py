import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt

print("Running file:", os.path.abspath(__file__))
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    print("Entered main()")
    if len(sys.argv) < 2:
        print("error: no prompt given"); sys.exit(1)

    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-1.5-flash-002",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    verbose = ("--verbose" in sys.argv[2:])

    um = response.usage_metadata    

    print(response.text or "[no text returned]")
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {um.prompt_token_count}")
        print(f"Response tokens: {um.candidates_token_count}")

    if response.candidates:
        fr = response.candidates[0].finish_reason
        print(f"Finish reason: {fr}")

if __name__ == "__main__":
    main()
