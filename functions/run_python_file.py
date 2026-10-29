import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_directory_abspath = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_directory_abspath, file_path)
        )

        if (
            os.path.commonpath((working_directory_abspath, target_file))
            != working_directory_abspath
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        # result is a CompletedProcess object
        result = subprocess.run(
            command,
            cwd=working_directory_abspath,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_list = []

        if result.returncode != 0:
            rc_string = f"Process exited with code {result.returncode}"
            output_list.append(rc_string)

        if not result.stdout and not result.stderr:
            no_output_string = "No output produced"
            output_list.append(no_output_string)
        else:
            if result.stdout:
                stdout_string = f"STDOUT: {result.stdout}"
                output_list.append(stdout_string)
            if result.stderr:
                stderr_string = f"STDERR: {result.stderr}"
                output_list.append(stderr_string)

        output_string = ("\n").join(output_list)
        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file within the working directory and returns its output, including stdout, stderr, and exit code information.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python file when executing it.",
                },
            },
            "required": ["file_path"],
        },
    },
}
