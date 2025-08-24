import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python
from functions.write_file import write_file, schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    calc_working_dir = "./calculator"
    kwargs = function_call_part.args

    func_output = ""

    match function_call_part.name:
        case "get_files_info":
            func_output = get_files_info(calc_working_dir, **kwargs)
        case "get_file_content":
            func_output = get_file_content(calc_working_dir, **kwargs)
        case "run_python_file":
            func_output = run_python_file(calc_working_dir, **kwargs)
        case "write_file":
            func_output = write_file(calc_working_dir, **kwargs)


def main():

    if len(sys.argv) < 2:
        sys.exit(1)
    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python,
            schema_write_file,
        ]
    )
        
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    function_call_part = response.function_calls

    for function_call in function_call_part:
        print(f"Calling function: {function_call.name}({function_call.args})")
    
    print(response.text)

    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
