import os


# List files
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

        return f'Success: "{directory}" is within the working directory'

    # Catch other errors gracefully
    except Exception as e:
        return f"Error: {e}"
