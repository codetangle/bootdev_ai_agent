from pathlib import Path
from functions.directory_helper import is_path_relative
from functions.directory_helper import get_app_directory

def get_files_info(working_directory, directory="."):
    working_dir_path = Path(working_directory)
    relative_path = Path(directory)
    full_path = working_dir_path / relative_path

    # validate path location
    app_dir = get_app_directory()
    is_path_dir = Path.is_dir(full_path)
    is_directory_relative = is_path_relative(full_path, app_dir)
    
    excluded_directories = ['.venv', '__pycache__']

    try:
        if is_directory_relative:
            if is_path_dir:
                if full_path.name in excluded_directories:
                    return f"Excluding {full_path.name}"
                else:
                    for dir_item in full_path.iterdir():
                        return get_file_stats(dir_item)
            else:
                raise Exception(f'Error: "{full_path}" is not a directory')
        else:
            raise Exception(f'Error: Cannot list "{full_path}" as it is outside the permitted working directory')
    except Exception as e:
        return e
    

def get_file_stats(file_object):
    is_path_dir = Path.is_dir(file_object)
    file_stats = file_object.stat()
    file_name = file_object.name
    file_data = f"- {file_name}: file_size={file_stats.st_size} bytes, is_dir={is_path_dir}"
        
    return file_data