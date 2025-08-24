from pathlib import Path
from google.genai import types
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

# Function declaration to pass to AI model
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content passed into the function to the file at the specified file path. If the file does not exist it is created. Any directories that do not exist are created. If the file exist, it will be overwritten.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file that the content is retrieved from, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the given file path.",
            ),
        },
        required=["file_path", "content"]
    ),
)