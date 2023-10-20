import argparse
import os
import gpxpy
import gpxpy.gpx


def densify_gpx_file(main_folder):
    # Recursively traverse the subfolders and process GPX files
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if file.endswith(".gpx"):
                print(f"Processing GPX file {file}", flush=True)
                gpx_file_path = os.path.join(root, file)

                # Open the GPX file
                with open(gpx_file_path, "r", encoding="utf-8") as gpx_file:
                    gpx = gpxpy.parse(gpx_file)

                total_points = 0
                for track in gpx.tracks:
                    for segment in track.segments:
                        total_points += len(segment.points)

                # Densify the GPX track
                progress, percent = 0, -1
                for track in gpx.tracks:
                    for segment in track.segments:
                        segment_points = segment.points
                        new_points = []
                        for i in range(len(segment_points) - 1):
                            point1 = segment_points[i]
                            point2 = segment_points[i + 1]
                            time1 = point1.time
                            time2 = point2.time
                            distance = point1.distance_2d(point2)
                            if distance > 0.1:  # Add a new point every 10cm
                                num_new_points = int(distance / 1)
                                for j in range(num_new_points):
                                    fraction = float(j + 1) / float(num_new_points + 1)
                                    lon = point1.longitude + fraction * (
                                        point2.longitude - point1.longitude
                                    )
                                    lat = point1.latitude + fraction * (
                                        point2.latitude - point1.latitude
                                    )
                                    time_diff = time2 - time1
                                    new_time = time1 + (time_diff * fraction)
                                    new_point = gpxpy.gpx.GPXTrackPoint(
                                        lat,
                                        lon,
                                        elevation=point1.elevation,
                                        time=new_time,
                                    )
                                    new_points.append(new_point)

                            progress += 1
                            if progress * 100 // total_points > percent:
                                percent = progress * 100 // total_points
                                print(
                                    f"\r[{'=' * percent}{' ' * (100 - percent)}] {percent}%",
                                    end="",
                                    flush=True,
                                )

                        if len(new_points) >= 2:
                            if len(segment_points) > 0:
                                # Add the first point to the new points list
                                new_points.insert(0, segment_points[0])
                                # Add the last point to the new points list
                                new_points.append(segment_points[-1])
                            # Replace the segment points with the new points
                            segment.points = new_points

                            # Save the densified GPX file
                            new_gpx_filename = file.split(".")[0] + "-OPTI.gpx"
                            new_gpx_filepath = os.path.join(root, new_gpx_filename)
                            with open(new_gpx_filepath, "w") as new_gpx_file:
                                new_gpx_file.write(gpx.to_xml())

                print(f"\r[{'=' * 100}] 100%", end="", flush=True)
                print()

    print("GPX files densified successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GPX densifier script")
    parser.add_argument(
        "folder", help="Path to the folder containing GPX files to process"
    )

    args = parser.parse_args()
    target_folder = args.folder

    densify_gpx_file(target_folder)
