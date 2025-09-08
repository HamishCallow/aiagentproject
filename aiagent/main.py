import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    verbose = ("--verbose" in sys.argv[2:])

    um = resp.usage_metadata    

    print(resp.text or "[no text returned]")
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {um.prompt_token_count}")
        print(f"Response tokens: {um.candidates_token_count}")

    if resp.candidates:
        fr = resp.candidates[0].finish_reason
        print(f"Finish reason: {fr}")

if __name__ == "__main__":
    main()