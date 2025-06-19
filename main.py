import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    prompt_parts = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not prompt_parts:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(prompt_parts)

    process_ai_interaction(client, user_prompt, verbose)


def process_ai_interaction(client, user_prompt: str, verbose: bool):
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    prompt_token_info = f"Prompt tokens: {response.usage_metadata.prompt_token_count}"
    response_token_info = (
        f"Response tokens: {response.usage_metadata.candidates_token_count}"
    )

    if verbose:
        print(prompt_token_info)
        print(response_token_info)
    else:
        print(response.text)


if __name__ == "__main__":
    main()
