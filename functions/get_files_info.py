import os

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, directory))

        if not abs_target.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory'

        lines = []
        for name in os.listdir(abs_target):
            full_path = os.path.join(abs_target, name)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path)
            lines.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"