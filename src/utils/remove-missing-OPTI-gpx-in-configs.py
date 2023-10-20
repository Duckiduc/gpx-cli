import os
import xml.etree.ElementTree as ET


def update_xml(xml_path, gpx_folder_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    to_remove = []

    track_config_list = root.find(
        "trackConfigurationList"
    )  # Assuming the trackConfigurationList is a child of the root

    for track_config in track_config_list.findall("trackConfiguration"):
        input_gpx = track_config.find("inputGpx").text
        gpx_file_path = os.path.join(gpx_folder_path, input_gpx)
        if not os.path.exists(gpx_file_path):
            to_remove.append(track_config)

    for track_config in to_remove:
        track_config_list.remove(track_config)

    tree.write(xml_path)


def process_folders(parent_folder):
    for dirpath, dirnames, filenames in os.walk(parent_folder):
        xml_files = [f for f in filenames if f.endswith(".xml")]
        for xml_file in xml_files:
            xml_path = os.path.join(dirpath, xml_file)
            gpx_folder_path = dirpath
            update_xml(xml_path, gpx_folder_path)


parent_folder_path = "../folder/videos_folder"
process_folders(parent_folder_path)
