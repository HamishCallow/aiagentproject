from config import MAX_CHARS
import os

def get_file_content(working_directory, file_path):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(abs_working, file_path))

        if not (abs_target == abs_working or abs_target.startswith(abs_working + os.sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_target, "r") as f:
            content = f.read(MAX_CHARS + 1)
            if len(content) >= MAX_CHARS + 1:
                return content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    
    except Exception as e:
        return f"Error: {e}"