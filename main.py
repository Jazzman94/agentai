import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
model_name = "gemini-2.0-flash-001"


if __name__ == "__main__":
    if len(sys.argv) == 2:
        content = sys.argv[1]
    else:
        print("Usage: python3 main.py <content>")
        sys.exit(1)

    response = client.models.generate_content(
        model=model_name,
        contents=content

    )
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


