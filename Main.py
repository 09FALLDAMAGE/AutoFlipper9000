import json
import os

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            return json.load(file)
    return {"default_project_path": "C:\\Programming\\Reefscape\\src\\main\\deploy\\pathplanner"}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file, indent=4)

def load_json(file_name):
    folder_path = "paths"  # Folder where JSON files are stored
    file_path = os.path.join(default_project_path, folder_path, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def extract_path_names(command_data):
    path_names = set()
    if isinstance(command_data, dict):
        if "type" in command_data and command_data["type"] == "path" and "data" in command_data and "pathName" in \
                command_data["data"]:
            path_names.add(command_data["data"]["pathName"])
        for key, value in command_data.items():
            path_names.update(extract_path_names(value))
    elif isinstance(command_data, list):
        for item in command_data:
            path_names.update(extract_path_names(item))
    return path_names


def find_deltas(json_data, ref_x, ref_y):
    deltas = []

    if "waypoints" in json_data:
        for waypoint in json_data["waypoints"]:
            for key in ["anchor", "prevControl", "nextControl"]:
                if key in waypoint and waypoint[key] is not None:
                    x, y = waypoint[key]["x"], waypoint[key]["y"]
                    delta_x = x - ref_x
                    delta_y = y - ref_y
                    deltas.append({"point": key, "x": x, "y": y, "delta_x": delta_x, "delta_y": delta_y})

    return deltas


def reflect_points(json_data, ref_x, ref_y, reflect_x=True, reflect_y=True, reflect_rotation_y=True,
                   reflect_rotation_x=True):
    reflected_data = json_data.copy()

    if "waypoints" in reflected_data:
        for waypoint in reflected_data["waypoints"]:
            waypoint["linkedName"] = None  # Set linkedName to null
            for key in ["anchor", "prevControl", "nextControl"]:
                if key in waypoint and waypoint[key] is not None:
                    if reflect_x:
                        waypoint[key]["x"] = 2 * ref_x - waypoint[key]["x"]
                    if reflect_y:
                        waypoint[key]["y"] = 2 * ref_y - waypoint[key]["y"]

    # Reflect rotation across y-axis
    if reflect_rotation_x:
        for state_key in ["idealStartingState", "goalEndState"]:
            if state_key in reflected_data and "rotation" in reflected_data[state_key]:
                reflected_data[state_key]["rotation"] = -reflected_data[state_key]["rotation"]

        if "rotationTargets" in reflected_data:
            for rotation_target in reflected_data["rotationTargets"]:
                if "rotationDegrees" in rotation_target:
                    rotation_target["rotationDegrees"] = -rotation_target["rotationDegrees"]

    # Reflect rotation across x-axis
    if reflect_rotation_y:
        for state_key in ["idealStartingState", "goalEndState"]:
            if state_key in reflected_data and "rotation" in reflected_data[state_key]:
                reflected_data[state_key]["rotation"] = -((reflected_data[state_key]["rotation"] + 180) % 360)

        if "rotationTargets" in reflected_data:
            for rotation_target in reflected_data["rotationTargets"]:
                if "rotationDegrees" in rotation_target:
                    rotation_target["rotationDegrees"] = -((rotation_target["rotationDegrees"] + 180) % 360)

    return reflected_data


def save_json(data, output_file):
    folder_path = "paths"
    file_path = os.path.join(default_project_path, folder_path, output_file)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def save_auto(data, output_file):
    folder_path = "autos"
    file_path = os.path.join(default_project_path, folder_path, output_file)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    settings = load_settings()
    default_project_path = settings["default_project_path"]

    if input(f"Current project path: {default_project_path}\nDo you want to change it? (y/n): ").strip().lower() == "y":
        default_project_path = input("Enter new project path: ").strip()
        settings["default_project_path"] = default_project_path
        save_settings(settings)


    command_folder_path = "autos"
    command_file = input("Enter Auto Name: ")  # JSON file containing path names
    with open(os.path.join(default_project_path, command_folder_path, command_file + ".auto"), 'r') as file:
        command_data = json.load(file)

    path_names = extract_path_names(command_data)
    print(f"Processing paths: {path_names}")

    # 8.774176 x 4.0259 y
    ref_x, ref_y = 8.77, 4.03

    # inputs for transformations
    reflect_x = input("Reflect across X-axis? (y/n): ").strip().lower() == "y"
    reflect_y = input("Reflect across Y-axis? (y/n): ").strip().lower() == "y"

    reflect_rotation_y = input("Reflect rotation fields across Y axis? (y/n): ").strip().lower() == "y"
    reflect_rotation_x = input("Reflect rotation fields across X axis? (y/n): ").strip().lower() == "y"

    prefix = input("Enter prefix for new paths: ").strip()
    suffix = input("Enter suffix for new paths: ").strip()
    command_prefix = input("Enter prefix for flipped commands file: ").strip()
    command_suffix = input("Enter suffix for flipped commands file: ").strip()

    flipped_commands = command_data.copy()

    for path_name in path_names:
        file_name = f"{path_name}.path"
        output_file = f"{prefix}{path_name}{suffix}.path"

        if os.path.exists(os.path.join(default_project_path, "paths", file_name)):
            json_data = load_json(file_name)
            deltas = find_deltas(json_data, ref_x, ref_y)
            reflected_data = reflect_points(json_data, ref_x, ref_y, reflect_x, reflect_y, reflect_rotation_y,
                                            reflect_rotation_x)
            save_json(reflected_data, output_file)

            for entry in deltas:
                print(
                    f"Point: {entry['point']}, X: {entry['x']}, Y: {entry['y']}, Delta X: {entry['delta_x']:.2f}, Delta Y: {entry['delta_y']:.2f}")
            print(f"Reflected data saved to {output_file}")

            # Update flipped_commands with new path names
            def update_command_paths(data):
                if isinstance(data, dict):
                    if "type" in data and data["type"] == "path" and "data" in data and "pathName" in data["data"]:
                        if data["data"]["pathName"] in path_names:
                            data["data"]["pathName"] = f"{prefix}{data['data']['pathName']}{suffix}"
                    for key, value in data.items():
                        update_command_paths(value)
                elif isinstance(data, list):
                    for item in data:
                        update_command_paths(item)

            update_command_paths(flipped_commands)
        else:
            print(f"File {file_name} not found in paths folder.")

    flipped_commands_file = f"{command_prefix}{command_suffix}.auto"
    save_auto(flipped_commands, flipped_commands_file)
    print(f"Flipped commands file saved to {flipped_commands_file}")
