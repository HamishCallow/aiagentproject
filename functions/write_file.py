import os
from google.genai import types

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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file's contents within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the target file within the working directory; must not escape it (no ../).",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file; creates or overwrites the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)