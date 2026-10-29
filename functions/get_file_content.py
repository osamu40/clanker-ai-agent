import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        path = os.path
        working_dir_abspath = path.realpath(path.abspath(working_directory))
        target_file = path.realpath(
            path.normpath(path.join(working_dir_abspath, file_path))
        )

        if working_dir_abspath != path.commonpath((working_dir_abspath, target_file)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return file_content_string

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Reads and returns the contents of the specified file, up to {MAX_CHARS} characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file, relative to the working directory",
                },
            },
        },
    },
}
