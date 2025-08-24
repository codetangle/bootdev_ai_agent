from sys import executable
from google.genai import types
from subprocess import run
from functions.directory_helper import is_path_relative, get_app_directory
from pathlib import Path

def run_python_file(working_directory, file_path, args=[]):
    try:
        return_val = ""
        working_path = Path(working_directory)
        file_obj = Path(file_path)
        full_path = working_path / file_obj
        app_dir = get_app_directory()

        is_work_dir_relative = is_path_relative(working_path, app_dir)
        is_file_relative = is_path_relative(full_path, working_path)
        
        path_relative = is_work_dir_relative and is_file_relative
        
        if not path_relative:
            raise Exception(f'Error: Cannot execute "{file_obj}" as it is outside the permitted working directory')
        
        if not full_path.exists():
            raise Exception(f'Error: File "{file_obj}" not found.')

        if not full_path.suffix == ".py":
            raise Exception(f'Error: "{file_obj}" is not a Python file.')
        
        command = [executable, full_path] + args
        result = run(command, capture_output=True, timeout=30, cwd=app_dir, text=True)

        std_out = f"STDOUT: {result.stdout}"
        std_err = f"STDERR: {result.stderr}"
        exit_code = f"Process exited with code {result.returncode}"
        return_values = [std_out, std_err, exit_code]

        if len(std_out) == 0:
            return_values.append(f"No output produced")
        return_val = '\n'.join(return_values)
    except Exception as e:
        return_val = f"Error: executing Python file: {e}"
        
    return return_val

# Function declaration to pass to AI model
schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python script at the file path given, supplied with the optional arguments. Scripts that can be run are limited to files relative to the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python script that will be run, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)
        