from pathlib import Path

def is_path_relative(child_path, parent_path):
    return str(child_path.resolve()).startswith(str(parent_path.resolve()))

def get_app_directory():
    return Path(__file__).parent.parent