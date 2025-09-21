import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
import json

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
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file]
    )

    response = client.models.generate_content(
        model="gemini-1.5-flash-002",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0,
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(mode="ANY")
            ),
        ),
    )

    calls = []
    if getattr(response, "function_calls", None):
        calls = response.function_calls
    elif response.candidates:
        for cand in response.candidates:
            if getattr(cand, "function_calls", None):
                calls = cand.function_calls
                break
    
    verbose = ("--verbose" in sys.argv[2:])

    if calls:
        for fc in calls:
            function_call_result = call_function(fc, verbose)
            
            if not (getattr(function_call_result, "parts", None) and len(function_call_result.parts) > 0):
                raise Exception("Fatal: call_function did not return expected 'parts' structure.")
            
            first_part = function_call_result.parts[0]

            if not getattr(first_part, "function_response", None):
                raise Exception("Fatal: call_function did not return expected 'function_response' structure.")
            
            function_response_obj = first_part.function_response
            
            if not getattr(function_response_obj, "response", None):
                raise Exception("Fatal: call_function did not return expected 'response' structure.")
            
            final_response = function_response_obj.response

            if verbose:
                print(f"-> {final_response}")
    else:
        print(response.text or "[no text returned]")

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
