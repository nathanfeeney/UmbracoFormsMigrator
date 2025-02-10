import json
import os
from lxml import etree

# Folder containing the .config files (update this to your folder path)
FOLDER_PATH = r"C:\PATH\TO\YOUR\FOLDER\PATH"  # Update this path

def transform_prevalues(obj):
    """Recursively searches for 'preValues' in JSON and reformats it."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "preValues" and isinstance(value, list) and all(isinstance(v, str) for v in value):
                print(f"DEBUG: Transforming preValues → {value}")
                obj[key] = [{"value": v, "sortOrder": i} for i, v in enumerate(value)]
            else:
                transform_prevalues(value)  # Recursively check nested dictionaries

    elif isinstance(obj, list):
        for item in obj:
            transform_prevalues(item)  # Recursively check each item in the list

def process_config_files():
    count = 0  # Initialize count
    if not os.path.exists(FOLDER_PATH):
        print(f"Folder not found: {FOLDER_PATH}")
        return

    files = [f for f in os.listdir(FOLDER_PATH) if f.endswith(".config")]
    
    if not files:
        print("No .config files found in the folder.")
        return
    
    for filename in files:
        file_path = os.path.join(FOLDER_PATH, filename)
        try:
            # Parse the XML file
            parser = etree.XMLParser(strip_cdata=False)  # Preserve CDATA
            tree = etree.parse(file_path, parser)
            root = tree.getroot()

            for pages_element in root.findall(".//Pages"):  # Adjust the tag name if necessary
                json_text = pages_element.text
                if json_text:
                    print(f"DEBUG: Extracted JSON from Pages → {json_text}")

                    try:
                        json_data = json.loads(json_text)

                        # Print full JSON for debugging
                        print(f"DEBUG: Full JSON Before Transformation → {json.dumps(json_data, indent=4)}")

                        # Transform preValues recursively
                        transform_prevalues(json_data)

                        # Print transformed JSON for debugging
                        print(f"DEBUG: Full JSON After Transformation → {json.dumps(json_data, indent=4)}")

                        # Convert back to JSON string
                        new_json_text = json.dumps(json_data, indent=4)

                        # Ensure CDATA wrapping
                        pages_element.text = etree.CDATA(new_json_text)
                        print(f"DEBUG: Updated JSON inside CDATA → {new_json_text}")

                    except json.JSONDecodeError:
                        print(f"Skipping {filename} - Invalid JSON inside XML.")
                        continue

            # Save modified XML back to file
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            print(f"Fixed: {filename}")

            count += 1

        except etree.XMLSyntaxError:
            print(f"Skipping {filename} - Not valid XML.")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"{count} .config files have been processed.")

# Run the script
process_config_files()
