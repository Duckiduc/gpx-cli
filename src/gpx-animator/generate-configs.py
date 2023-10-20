import os
import xml.etree.ElementTree as ET

# Path to the main folder containing subfolders
main_folder = "../folder/videos_folder"

# Iterate over the subfolders
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)

    # Check if the item is a subfolder
    if os.path.isdir(subfolder_path):
        # Create the XML structure
        config = ET.Element("configuration")
        ET.SubElement(config, "margin").text = "20"
        ET.SubElement(config, "width").text = "1920"
        ET.SubElement(config, "height").text = "1200"
        ET.SubElement(config, "viewportWidth").text = "1920"
        ET.SubElement(config, "viewportHeight").text = "1200"
        ET.SubElement(config, "viewportInertia").text = "50"
        ET.SubElement(config, "preDrawTrack").text = "false"
        ET.SubElement(config, "speedup").text = "1.0"
        ET.SubElement(config, "tailDuration").text = "1000"
        ET.SubElement(config, "tailColor").text = "#FF006666"
        ET.SubElement(config, "tailColorFadeout").text = "true"
        ET.SubElement(config, "fps").text = "30.0"
        ET.SubElement(config, "backgroundMapVisibility").text = "0.0"
        ET.SubElement(
            config, "tmsUrlTemplate"
        ).text = "https://{switch:a,b,c}.tile.opentopomap.org/{zoom}/{x}/{y}.png"
        ET.SubElement(config, "tmsApiKey").text = "975afe21b545a7313b275235026490b"
        ET.SubElement(config, "tmsUserAgent").text = ""
        ET.SubElement(config, "skipIdle").text = "true"
        ET.SubElement(config, "backgroundColor").text = "#FF00CC33"
        ET.SubElement(config, "flashbackColor").text = "#FFFFFFFF"
        ET.SubElement(config, "flashbackDuration").text = "1000"
        ET.SubElement(
            config, "output"
        ).text = f"./Animation_suhain_petit_FV_{subfolder}.mp4"
        ET.SubElement(config, "videoCodec").text = "H264"
        ET.SubElement(
            config, "attribution"
        ).text = "Created by %APPNAME_VERSION% %MAP_ATTRIBUTION%"
        ET.SubElement(config, "attributionPosition").text = "BOTTOM_LEFT"
        ET.SubElement(config, "attributionMargin").text = "20"
        ET.SubElement(config, "information").text = "%SPEED% %LATLON% %DATETIME%"
        ET.SubElement(config, "informationPosition").text = "BOTTOM_RIGHT"
        ET.SubElement(config, "informationMargin").text = "20"
        ET.SubElement(config, "commentPosition").text = "BOTTOM_CENTER"
        ET.SubElement(config, "commentMargin").text = "20"
        ET.SubElement(config, "font").text = "Monospaced-PLAIN-12"
        ET.SubElement(config, "markerSize").text = "8.0"
        ET.SubElement(config, "waypointFont").text = "Monospaced-PLAIN-12"
        ET.SubElement(config, "waypointSize").text = "6.0"
        ET.SubElement(config, "minLon").text = "98.96361"
        ET.SubElement(config, "maxLon").text = "99.14061"
        ET.SubElement(config, "minLat").text = "44.04799"
        ET.SubElement(config, "maxLat").text = "44.15159"
        ET.SubElement(config, "logoPosition").text = "TOP_LEFT"
        ET.SubElement(config, "logoMargin").text = "20"
        ET.SubElement(config, "photoTime").text = "3000"
        ET.SubElement(config, "photoAnimationDuration").text = "700"
        ET.SubElement(config, "speedUnit").text = "KMH"
        ET.SubElement(config, "gpsTimeout").text = "60000"

        # Read the template XML file
        template_file_path = (
            "./template-config-hajuu-petit.xml"  # Path to your template XML file
        )
        template_tree = ET.parse(template_file_path)
        template_root = template_tree.getroot()

        # Create trackConfigurationList element
        track_config_list = ET.SubElement(config, "trackConfigurationList")

        # Update inputGpx and output values
        for track_config in template_root.iter("trackConfiguration"):
            input_gpx = track_config.find("inputGpx")
            if input_gpx is not None:
                input_gpx.text = input_gpx.text.replace(
                    ".gpx", f"_{subfolder}-OPTI.gpx"
                )

            output = track_config.find("output")
            if output is not None:
                output.text = output.text.replace(".mp4", f"_{subfolder}.mp4")

            track_config_list.append(track_config)

        # Save the XML file
        xml_file_name = f"GPX_ANIMATOR_CONFIG_{subfolder}.ga.xml"
        xml_file_path = os.path.join(subfolder_path, xml_file_name)
        ET.ElementTree(config).write(
            xml_file_path, encoding="utf-8", xml_declaration=True
        )

print("XML files created successfully!")
