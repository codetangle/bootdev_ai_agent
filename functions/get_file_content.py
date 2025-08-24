from google.genai import types
from functions.config import max_characters_read
from functions.directory_helper import get_app_directory
from functions.directory_helper import is_path_relative
from pathlib import Path



def get_file_content(working_directory, file_path):
    dir_obj = Path(working_directory)
    file_obj = Path(file_path)
    full_path = dir_obj / file_obj
    app_directory = get_app_directory()

    try:
        if is_path_relative(full_path, app_directory):
            if full_path.is_file():
                with open(full_path) as f:
                    content = f.read(max_characters_read)
                    if len(content) == max_characters_read:
                        content += f"\n[...File \"{file_path}\" truncated at {max_characters_read} characters]"
                    return content
            else:
                raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
        else:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    except Exception as e:
        return str(e)

# Function declaration to pass to AI model
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of the specified file in the specified directory, output is limited to 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file that the content is retrieved from, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)