import argparse
import os
import gpxpy


def reorder_track_points(track_segment):
    track_segment.points.sort(key=lambda pt: pt.time)


def process_gpx_file(file_path):
    with open(file_path, "r", encoding="utf-8") as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                reorder_track_points(segment)

    with open(file_path, "w", encoding="utf-8") as updated_gpx_file:
        updated_gpx_file.write(gpx.to_xml())


def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".gpx"):
                file_path = os.path.join(root, filename)
                process_gpx_file(file_path)
                print(f"Reordered track points in {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GPX points reordering script")
    parser.add_argument(
        "folder", help="Path to the folder containing GPX files to process"
    )

    args = parser.parse_args()
    target_folder = args.folder

    process_folder(target_folder)
