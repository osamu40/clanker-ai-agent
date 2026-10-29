import os

path = os.path


def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        working_dir_abspath = path.abspath(working_directory)
        target_file = path.realpath(
            path.normpath(path.join(working_dir_abspath, file_path))
        )

        if working_dir_abspath != path.commonpath((working_dir_abspath, target_file)):
            return f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory'

        if path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Sucessfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes given content to a specified file, creating it if it doesn't exist, relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write into the file.",
                },
            },
        },
    },
}
