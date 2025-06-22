import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Add the 'functions' directory to the Python path at the very beginning.
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "functions"))
)

# Import the new call_function from your functions directory
from call_function import call_function


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

    # Define the schema for all available functions.
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
        description="Reads the content of a specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to read, relative to the working directory.",
                ),
            },
            required=["file_path"],
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file within the working directory with a 30-second timeout. Captures stdout and stderr.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to execute, relative to the working directory.",
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    description="Optional list of string arguments to pass to the Python script.",
                    items=types.Schema(type=types.Type.STRING),
                ),
            },
            required=["file_path"],
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes or overwrites content to a file, creating parent directories if necessary, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write to, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content string to write to the file.",
                ),
            },
            required=["file_path", "content"],
        ),
    )

    available_tools = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    # --- CRITICAL FIX: Further refined system prompt for structured final response ---
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, your primary goal is to make a direct and relevant function call plan without unnecessary preliminary steps (like listing files if the intent is clearly to act on one). You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

**IMPORTANT PATH GUIDANCE:** All paths you provide in function calls MUST be relative to the **project root** (the directory where main.py resides).

**File Locations and Context:**
- The following files are located directly in the project root: `main.py`, `requirements.txt`, `.env`, `README.md`, `tests.py`, `.gitignore`
- The `calculator` subdirectory contains files like `main.py`, `README.md`, `tests.py`, and the `pkg` subdirectory (which holds `lorem.txt`, `calculator.py`, and `render.py` within `calculator/pkg/`).

**When analyzing code (e.g., how something is rendered):**
1.  Start by reading the `main.py` file of the relevant application (e.g., `calculator/main.py`).
2.  Examine its imports and function calls. If it imports or calls a function related to the task (like a 'render' function), identify the module/file where that function is defined.
3.  Read the content of that identified module/file to understand the implementation details.
4.  Once you have gathered sufficient information to answer the user's question, provide a clear, concise explanation. **Your final explanation should be structured, using numbered lists or clear paragraphs to break down the process step-by-step, similar to a detailed code review.** Do not stop until you have found the specific code responsible for the requested action.

**Special Handling for "what files are in the root?":**
When asked "what files are in the root?", you must provide a comprehensive list of all *relevant* files in the project's primary context. This means you should first call `get_files_info(directory='.')` to list files in the main project directory. Immediately after this, you **must also call `get_files_info(directory='calculator')`** to include important files from that subdirectory. Your final output should reflect the information from both of these calls.

**Examples of CORRECT path usage for direct action:**
- To list files in the 'calculator' directory: `get_files_info(directory='calculator')`
- To list files in the root directory: `get_files_info(directory='.')`
- To read 'lorem.txt' (which is in 'calculator/'): `get_file_content(file_path='calculator/lorem.txt')`
- To read 'main.py' (which is in 'calculator/'): `get_file_content(file_path='calculator/main.py')`
- To read 'pkg/render.py' (which is in 'calculator/pkg/'): `get_file_content(file_path='calculator/pkg/render.py')`
- To run 'tests.py' (which is in 'calculator/'): `run_python_file(file_path='calculator/tests.py')`
- To run the main project tests.py file: `run_python_file(file_path='tests.py')`
- To write to 'new_file.txt' in the root: `write_file(file_path='new_file.txt', content='some text')`
- To write to 'pkg/another_file.txt' (within 'calculator/pkg/'): `write_file(file_path='calculator/pkg/another_file.txt', content='more text')`

You do not need to specify the top-level 'working_directory' argument in your function calls, as it is automatically injected for security reasons.
"""
    # --- END CRITICAL FIX ---

    # Initialize messages list ONLY with the user's initial prompt.
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # AGENTIC LOOP START
    for i in range(20):
        if verbose:
            print(f"\n--- Agent Iteration {i+1} ---")
            print(f"Current messages in conversation: {len(messages)}")

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_tools],
                system_instruction=system_prompt,
                temperature=0.0,
            ),
        )

        if verbose:
            prompt_token_info = (
                f"Prompt tokens: {response.usage_metadata.prompt_token_count}"
            )
            response_token_info = (
                f"Response tokens: {response.usage_metadata.candidates_token_count}"
            )
            print(prompt_token_info)
            print(response_token_info)

        if not (
            response.candidates
            and response.candidates[0].content
            and response.candidates[0].content.parts
        ):
            print("\nFinal response:")
            print("No valid response content received from the AI (breaking loop).")
            break

        model_response_content = response.candidates[0].content
        messages.append(model_response_content)

        has_function_call_this_turn = False
        final_text_response_content = None

        for part in model_response_content.parts:
            if part.function_call:
                has_function_call_this_turn = True

                print(f" - Calling function: {part.function_call.name}")

                function_call_result = call_function(
                    part.function_call, verbose=verbose
                )

                if not (
                    function_call_result.parts
                    and function_call_result.parts[0].function_response
                    and function_call_result.parts[0].function_response.response
                ):
                    raise RuntimeError(
                        f"Unexpected function call result format: {function_call_result}"
                    )

                result_content = function_call_result.parts[
                    0
                ].function_response.response

                if verbose:
                    print(f"-> {result_content}")
                else:
                    print(result_content)

                messages.append(function_call_result)
                break

            elif part.text:
                final_text_response_content = part.text
                if not verbose and not has_function_call_this_turn:
                    print(part.text)

        if not has_function_call_this_turn:
            print("\nFinal response:")
            if final_text_response_content:
                print(final_text_response_content)
            else:
                print("Agent finished without a clear text response.")
            break

    else:
        print("\nMax iterations (20) reached. Agent stopped without concluding.")
        if messages and messages[-1].parts and messages[-1].parts[0].text:
            print(f"Last message from agent: {messages[-1].parts[0].text}")
        else:
            print("No final text response from agent at max iterations.")


if __name__ == "__main__":
    main()
