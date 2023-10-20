import os
import subprocess
import json
import csv
from datetime import datetime, timedelta

# Path to the directory containing video files
directory = "../folder/videos_folder"

# Path to the output CSV file
output_file = "../folder/output.csv"

# List to store metadata
metadata_list = []

# Iterate over video files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".MOV"):
        video_path = os.path.join(directory, filename)

        # Execute ffprobe command to get video metadata as JSON
        command = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            video_path,
        ]
        result = subprocess.check_output(command).decode("utf-8")

        # Parse the JSON output
        metadata = json.loads(result)
        metadata_list.append(metadata)

# Extract desired metadata fields and calculate end date
with open(output_file, "w", newline="") as csvfile:
    fieldnames = [
        "Filename",
        "Duration",
        "Width",
        "Height",
        "Creation Date ",
        "End Date",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for metadata in metadata_list:
        video_data = {}
        video_data["Filename"] = os.path.basename(metadata["format"]["filename"])
        video_data["Duration"] = metadata["format"]["duration"]
        video_data["Width"] = metadata["streams"][0]["width"]
        video_data["Height"] = metadata["streams"][0]["height"]

        creation_date_str = metadata["format"]["tags"].get("creation_time")
        if creation_date_str:
            creation_date = datetime.strptime(
                creation_date_str, "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            duration = timedelta(seconds=float(metadata["format"]["duration"]))
            end_date = creation_date + duration
            video_data["Creation Date"] = creation_date.strftime("%Y-%m-%d %H:%M:%S")
            video_data["End Date"] = end_date.strftime("%Y-%m-%d %H:%M:%S")

        writer.writerow(video_data)

print("Metadata exported to CSV successfully!")
