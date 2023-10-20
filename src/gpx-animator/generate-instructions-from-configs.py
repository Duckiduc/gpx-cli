import os
import xml.etree.ElementTree as ET


def convert_xml_to_command(xml_filename):
    tree = ET.parse(xml_filename)
    root = tree.getroot()

    # Location of the JAR file
    command = ["java -jar ../folder/gpx-animator-1.8.2-all.jar"]

    property_mappings = {
        "attribution": "attribution",
        "attributionPosition": "attribution-position",
        "attributionMargin": "attribution-margin",
        "backgroundColor": "background-color",
        "backgroundImage": "background-image",
        "backgroundMapVisibility": "background-map-visibility",
        "color": "color",
        # "flashbackColor": "flashback-color",
        "flashbackDuration": "flashback-duration",
        "font": "font",
        "forcedPointTimeInterval": "forced-point-time-interval",
        "fps": "fps",
        "gui": "gui",
        "height": "height",
        "help": "help",
        "inputGpx": "input",
        "trimGpxStart": "trim-gpx-start",
        "trimGpxEnd": "trim-gpx-end",
        # "information": "information",
        # "informationPosition": "information-position",
        # "informationMargin": "information-margin",
        "commentPosition": "comment-position",
        "commentMargin": "comment-margin",
        "trackIcon": "track-icon",
        "trackIconFile": "track-icon-file",
        "trackIconMirror": "track-icon-mirror",
        "inputEndIcon": "input-end-icon",
        "keepFirstFrame": "keep-first-frame",
        "keepLastFrame": "keep-last-frame",
        "label": "label",
        "lineWidth": "line-width",
        "logoPosition": "logo-position",
        "logoMargin": "logo-margin",
        "margin": "margin",
        "markerSize": "marker-size",
        "minLat": "min-lat",
        "maxLat": "max-lat",
        "minLon": "min-lon",
        "maxLon": "max-lon",
        "output": "output",
        "photoTime": "photo-time",
        "photoDir": "photo-dir",
        # "preDrawTrack": "pre-draw-track",
        # "preDrawTrackColor": "pre-draw-track-color",
        "skipIdle": "skip-idle",
        "speedup": "speedup",
        "tailDuration": "tail-duration",
        # "tailColor": "tail-color",
        # "tailColorFadeout": "tail-color-fadeout",
        "timeOffset": "time-offset",
        "tmsUrlTemplate": "tms-url-template",
        "tmsApiKey": "tms-api-key",
        "tmsUserAgent": "tms-user-agent",
        "totalTime": "total-time",
        "speedUnit": "speed-unit",
        "viewportWidth": "viewport-width",
        "viewportHeight": "viewport-height",
        "viewportInertia": "viewport-inertia",
        "waypointSize": "waypoint-size",
        "width": "width",
        "zoom": "zoom",
        "gpsTimeout": "gps-timeout",
        "version": "version",
    }

    for elem in root.iter("configuration"):
        for child_elem in elem:
            tag = child_elem.tag
            prop_name = property_mappings.get(tag)
            if tag == "trackConfigurationList":
                for track_config_elem in child_elem.findall("trackConfiguration"):
                    for prop_elem in track_config_elem:
                        tag = prop_elem.tag
                        prop_name = property_mappings.get(tag)
                        if prop_name is None:
                            continue
                        # elif prop_name == "color" or prop_name == "background-color":
                        #     command.append(f'--{prop_name} {prop_elem.text}')
                        #     continue
                        prop_value = prop_elem.text

                        if prop_value:
                            command.append(f'--{prop_name} "{prop_value}"')
            elif prop_name is None:
                continue
            else:
                print(prop_name)
                prop_value = child_elem.text

                if prop_value:
                    command.append(f'--{prop_name} "{prop_value}"')

    return " ".join(command)


def process_folders(parent_folder):
    for dirpath, dirnames, filenames in os.walk(parent_folder):
        xml_files = [f for f in filenames if f.endswith(".xml")]
        for xml_file in xml_files:
            xml_path = os.path.join(dirpath, xml_file)
            command = convert_xml_to_command(xml_path)

            # Create the "command" file in the same directory as the XML file
            command_file_path = os.path.join(dirpath, "command")
            with open(command_file_path, "w") as command_file:
                command_file.write(command)

            print(f"Command written to '{command_file_path}' file.")


parent_folder_path = "../folder/videos_folder"
process_folders(parent_folder_path)
