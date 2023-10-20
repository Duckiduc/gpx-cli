import os


def delete_opti_files(folder_path):
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith("OPTI.gpx"):
                file_path = os.path.join(root, filename)
                os.remove(file_path)
                print(f"Deleted {filename}")


target_folder = "../folder"
delete_opti_files(target_folder)
