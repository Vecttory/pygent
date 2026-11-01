import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path[-3:] == '.py':
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        result = subprocess.run(
            args=command, text=True, timeout=30, capture_output=True)

        result_code = result.returncode
        result_out = result.stdout
        result_err = result.stderr

        response: list[str] = []

        if result_code != 0:
            response.append(f"Process exited with code {result_code}")

        if not result_err and not result_out:
            print(result_err, "<->", result_out)
            print(bool(result_err), "<->", bool(result_out))
            response.append("No output produced")

        if result_out:
            response.append(f"STDOUT: {result_out}")

        if result_err:
            response.append(f"STDERR: {result_err}")

        return "\n".join(response)

    except Exception as err:
        return (f"Error: executing Python file: {err}")
