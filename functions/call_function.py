from google.genai import types

# Import all the tool functions that the agent can call
from get_files_info import get_files_info
from get_file_content import get_file_content
from run_python import run_python_file
from write_file import write_file

# Define the fixed working directory for all tool calls
# CRITICAL FIX Set to '.' (the project root) to align with LLM's relative path understanding.
AGENT_WORKING_DIRECTORY = "."


def call_function(
    function_call_part: types.FunctionCall, verbose: bool = False
) -> types.Content:
    """
    Handles the execution of a function requested by the LLM.

    Args:
        function_call_part: A types.FunctionCall object containing the
                            name of the function to call and its arguments.
        verbose: If True, prints detailed information about the function call.

    Returns:
        A types.Content object containing the result of the function call,
        formatted as a tool response.
    """
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)  # Convert to a mutable dict

    # Dictionary mapping function names (strings) to the actual function objects
    available_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    # Add the hardcoded working_directory to the arguments.
    # The LLM doesn't control this for security and consistency.
    function_args["working_directory"] = AGENT_WORKING_DIRECTORY

    # Print verbose output if requested
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        pass  # Output is controlled by main.py after the call

    # Check if the requested function name is valid
    if function_name not in available_functions:
        # Return an error indicating an unknown function
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Get the actual function object
    func_to_call = available_functions[function_name]

    # Call the function and capture its result
    try:
        # The ** operator unpacks the dictionary into keyword arguments
        function_result = func_to_call(**function_args)
    except Exception as e:
        # Catch any unexpected errors during function execution and return them
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing {function_name}: {e}"},
                )
            ],
        )

    # Return the result as a types.Content object from a function response.
    # The assignment specifies shoving the string result into a "result" field.
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
