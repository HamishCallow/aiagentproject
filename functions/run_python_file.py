import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(abs_working, file_path))
        
        if not abs_target.startswith(abs_working + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_target):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        result = subprocess.run(["python", file_path, *args], capture_output=True, timeout=30, cwd=working_directory)
        stdout_text = result.stdout.decode()
        stderr_text = result.stderr.decode()
        exit_code = result.returncode

        if not stdout_text and not stderr_text:
            return "No output produced."
        
        if exit_code != 0:
            return f"STDOUT: {stdout_text}\nSTDERR: {stderr_text}\nProcess exited with code {exit_code}"
        
        return f"STDOUT: {stdout_text}\nSTDERR: {stderr_text}"
    
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file within the working directory; must not escape it (no ../).",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments passed to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)