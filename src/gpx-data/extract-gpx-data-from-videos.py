import os
import csv
from datetime import datetime, timedelta, timezone
import gpxpy
import gpxpy.gpx

# Path to the exported CSV file
csv_file = "../folder/output.csv"

# Path to the folder containing GPX files
gpx_folder = "../folder/gpx_folder"

# Read the CSV file
video_data = []
with open(csv_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        video_data.append(row)

# Process video data and export GPX files
for video in video_data:
    video_name = video["Filename"].split(".")[0]
    video_folder = os.path.join(gpx_folder, video_name)
    os.makedirs(video_folder, exist_ok=True)

    # Parse the dates
    creation_date = datetime.strptime(video["Creation Date"], "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(video["End Date"], "%Y-%m-%d %H:%M:%S")

    # Subtract 4 minutes from the creation date and add 4 minutes to the end date
    creation_date -= timedelta(minutes=4)
    end_date += timedelta(minutes=4)

    # Convert creation_date and end_date to offset-aware datetimes
    utc_offset = creation_date.replace(tzinfo=timezone.utc).astimezone().utcoffset()
    creation_date = creation_date.replace(tzinfo=timezone.utc) - utc_offset
    end_date = end_date.replace(tzinfo=timezone.utc) - utc_offset

    # Iterate over GPX files
    for gpx_filename in os.listdir(gpx_folder):
        if gpx_filename.endswith(".gpx"):
            gpx_file_path = os.path.join(gpx_folder, gpx_filename)

            # Create a new GPX object
            gpx = gpxpy.gpx.GPX()

            # Open the existing GPX file
            with open(gpx_file_path, "r") as gpx_file:
                gpx_data = gpx_file.read()

            # Parse the GPX data
            gpx_obj = gpxpy.parse(gpx_data)

            # Iterate over tracks and add the points to the new GPX object
            for track in gpx_obj.tracks:
                new_track = gpxpy.gpx.GPXTrack()
                gpx.tracks.append(new_track)

                # Iterate over segments and add the points to the new track
                for segment in track.segments:
                    new_segment = gpxpy.gpx.GPXTrackSegment()
                    new_track.segments.append(new_segment)

                    # Iterate over points and add them to the new segment if within the date range
                    points = segment.points

                    for i, point in enumerate(points):
                        if creation_date <= point.time <= end_date:
                            new_segment.points.append(point)

                            # Check if previous point should be included
                            if i > 0 and point.time > creation_date:
                                new_segment.points.append(points[i - 1])

                            # Check if next point should be included
                            if i < len(points) - 1 and point.time < end_date:
                                new_segment.points.append(points[i + 1])

            # Export the new GPX file
            new_gpx_filename = gpx_filename.split(".")[0] + "_" + video_name + ".gpx"
            new_gpx_filepath = os.path.join(video_folder, new_gpx_filename)
            with open(new_gpx_filepath, "w") as new_gpx_file:
                new_gpx_file.write(gpx.to_xml())

print("GPX files exported successfully!")
