import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
model_name = "gemini-2.0-flash-001"

system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
When the user asks for files in the root directory, you should call get_files_info with the directory parameter set to '.'.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file in file_path with the specified content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write or overwrite, relative to the working directory. If the file does not exist, it will be created.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. If the file already exists, it will be overwritten by this content.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part: types.FunctionCall, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")
    
    args["working_directory"] = "./calculator"

    if function_name == "get_files_info":
        response = get_files_info(**args)
    elif function_name == "get_file_content":
        response = get_file_content(**args)
    elif function_name == "run_python_file":
        response = run_python_file(**args)
    elif function_name == "write_file":
        response = write_file(**args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": response},
            )
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate content using Gemini AI')
    parser.add_argument('prompt', help='The prompt to send to the AI')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose output with token usage information')
    
    args = parser.parse_args()
    prompt = args.prompt

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose=args.verbose)
            if not function_call_result.parts[0].function_response.response:
                raise ValueError(f"Function {function_call_part.name} returned no response")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
    else:
        print(response.text)
    
    
    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


