import os
import subprocess
import concurrent.futures


def run_command(command, working_dir):
    try:
        subprocess.run(command, shell=True, check=True, cwd=working_dir)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code: {e.returncode}")
    except Exception as e:
        print(f"Error occurred while running command: {e}")


def run_commands_in_folders(parent_folder, max_workers=6):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for dirpath, dirnames, filenames in os.walk(parent_folder):
            command_files = [f for f in filenames if f == "command"]
            for command_file in command_files:
                command_file_path = os.path.join(dirpath, command_file)
                with open(command_file_path, "r") as f:
                    command = f.read().strip()

                print(f"Running command from '{command_file_path}':\n{command}")
                executor.submit(run_command, command, dirpath)
                print()


parent_folder_path = "../folder/videos_folder"
run_commands_in_folders(parent_folder_path, max_workers=6)
