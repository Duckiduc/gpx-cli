import re
import gpxpy
from datetime import datetime

# Open the GPX file
with open("file.gpx", "r") as f:
    gpx = gpxpy.parse(f)

# Define the regex pattern to match the time value
pattern = r"<time>(.+)</time>"

# Loop through the track points and update the time format
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            # Extract the time value using regex
            match = re.search(pattern, str(point))
            if match:
                time_str = match.group(1)
                time_obj = datetime.strptime(time_str, "%m/%d/%YT%H:%M:%SZ")

                # Format the time in the desired format
                time_formatted = time_obj.strftime("%Y:%m:%d %H:%M:%S %z")

                # Add a new element for the updated time value
                point.extensions.append("<time>{}</time>".format(time_formatted))

                # Remove the original time element
                for ext in point.extensions:
                    if "<time>" in ext:
                        point.extensions.remove(ext)
                        break

# Save the updated GPX file
with open("output_file.gpx", "w") as f:
    f.write(gpx.to_xml())
