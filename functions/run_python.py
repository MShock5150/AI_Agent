import os
import subprocess
import sys


# Helper function to resolve paths and check scope for execution operations.
def _resolve_and_check_scope(working_directory, target_path_str):
    """
    Resolves the target_path_str relative to working_directory,
    and checks if the resolved path is within the working_directory's scope.
    Returns the absolute resolved path if valid, or an error string if out of scope.
    """
    abs_working_dir = os.path.abspath(working_directory)

    combined_path = os.path.join(abs_working_dir, target_path_str)
    abs_resolved_path = os.path.abspath(combined_path)

    if os.path.commonpath([abs_working_dir, abs_resolved_path]) != abs_working_dir:
        return f'Error: Cannot execute "{target_path_str}" as it is outside the permitted working directory'

    return abs_resolved_path


def run_python_file(working_directory, file_path):
    # Step 1: Resolve the file_path and perform initial security scope check.
    resolved_path_or_error = _resolve_and_check_scope(working_directory, file_path)

    if isinstance(resolved_path_or_error, str) and resolved_path_or_error.startswith(
        "Error:"
    ):
        return resolved_path_or_error

    abs_file_full_path = resolved_path_or_error
    abs_working_dir_for_subprocess = os.path.abspath(working_directory)

    # Step 2: Implement further checks for file existence and Python file extension.
    if not os.path.isfile(abs_file_full_path):
        # CRITICAL FIX for CLI test: Use os.path.basename for the error message
        # as the CLI test seems to expect the filename without the directory prefix.
        return f'Error: File "{os.path.basename(file_path)}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    # Step 3: Execute the Python file using subprocess.run.
    output_lines = []

    try:
        command = [sys.executable, abs_file_full_path]

        process_result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir_for_subprocess,
        )

        if process_result.stdout:
            output_lines.append("STDOUT:")
            output_lines.append(process_result.stdout.strip())

        if process_result.stderr:
            output_lines.append("STDERR:")
            output_lines.append(process_result.stderr.strip())

        if process_result.returncode != 0:
            output_lines.append(f"Process exited with code {process_result.returncode}")

        if not output_lines:
            return "No output produced."

        return "\n".join(output_lines)

    except subprocess.TimeoutExpired as e:
        output_lines.append("Error: Process timed out after 30 seconds.")
        if e.stdout:
            output_lines.append("STDOUT (before timeout):")
            output_lines.append(e.stdout.strip())
        if e.stderr:
            output_lines.append("STDERR (before timeout):")
            output_lines.append(e.stderr.strip())
        return "\n".join(output_lines)

    except OSError as e:
        return f"Error: executing Python file: {e}"

    except Exception as e:
        return f"Error: an unexpected error occurred: {e}"
