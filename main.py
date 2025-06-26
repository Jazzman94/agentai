import os
import argparse
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
model_name = "gemini-2.0-flash-001"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate content using Gemini AI')
    parser.add_argument('prompt', help='The prompt to send to the AI')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose output with token usage information')
    
    args = parser.parse_args()
    prompt = args.prompt

    messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)]),]

    response = client.models.generate_content(
        model=model_name,
        contents=messages

    )
    print(response.text)
    
    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


