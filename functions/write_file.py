import os

def write_file(working_directory, file_path, content):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(abs_working, file_path))
        parent_dir = os.path.dirname(abs_target)

        if not abs_target.startswith(abs_working + os.sep):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        
        with open(abs_target, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"