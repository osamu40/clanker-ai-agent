import os


# Validate Path
def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        path = os.path

        working_directory_abspath = path.abspath(working_directory)
        target_dir = path.normpath(path.join(working_directory_abspath, directory))

        # Check if target directory falls under absolute path
        if working_directory_abspath != path.commonpath(
            (
                working_directory_abspath,
                target_dir,
            )
        ):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the specified directory is a valid directory
        if not path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        return list_files(target_dir)

    # Catch other errors gracefully
    except Exception as e:
        return f"Error: {e}"


# List Files
def list_files(target_directory) -> str:
    try:
        dir_items = os.listdir(target_directory)
        dir_info = []

        for item in dir_items:
            name = item
            path = target_directory + "/" + name
            size = os.path.getsize(path)
            is_dir = False

            if os.path.isdir(path):
                is_dir = True

            file_info_string = f" - {name}: file_size={size} bytes, is_dir={is_dir}"
            dir_info.append(file_info_string)

        data_string = ("\n").join(dir_info)
        return data_string

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
