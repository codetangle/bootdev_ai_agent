from pathlib import Path
from functions.directory_helper import is_path_relative, get_app_directory

def write_file(working_directory, file_path, content):
    try:
        working_dir_path = Path(working_directory)
        file_obj = Path(file_path)
        full_path = working_dir_path / file_obj
        app_dir = get_app_directory()
        return_val = f"Failed to write to {full_path} content"

        if is_path_relative(full_path, app_dir):
            if full_path.is_dir():
                full_path.mkdir(parents=True, exist_ok=True)
            elif full_path.is_file():
                full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
                return_val = f'Successfully wrote to "{full_path}" {len(content)} characters written)'
        else:
            raise Exception(f'Cannot write to "{full_path}" as it is outside the permitted working directory')
    except Exception as e:
        return_val = f"Error: {e}"
    return return_val