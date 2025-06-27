import os
import subprocess


def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_dir):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        output = subprocess.run(['python3',file_path], capture_output=True, timeout=30, cwd = abs_working_dir)
        result_lines = []

        if output.stdout:
            result_lines.append("STDOUT:")
            result_lines.append(output.stdout.decode('utf-8'))

        if output.stderr:
            result_lines.append("STDERR:")
            result_lines.append(output.stderr.decode('utf-8'))

        if output.returncode != 0:
            result_lines.append(f"Process exited with code {output.returncode}")

        final_output = "\n".join(result_lines)

        if len(result_lines) == 0:
            return "No output produced"
 
        return final_output
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

    