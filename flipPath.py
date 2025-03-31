import json
import os


def load_json(file_name):
    folder_path = "paths"  # Folder where JSON files are stored
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


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


def reflect_points(json_data, ref_x, ref_y, reflect_x=True, reflect_y=True, reflect_rotation=True,
                   reflect_rotation_degrees=True):
    reflected_data = json_data.copy()

    if "waypoints" in reflected_data:
        for waypoint in reflected_data["waypoints"]:
            for key in ["anchor", "prevControl", "nextControl"]:
                if key in waypoint and waypoint[key] is not None:
                    if reflect_x:
                        waypoint[key]["x"] = 2 * ref_x - waypoint[key]["x"]
                    if reflect_y:
                        waypoint[key]["y"] = 2 * ref_y - waypoint[key]["y"]

    # Reflect rotation fields
    if reflect_rotation:
        for state_key in ["idealStartingState", "goalEndState"]:
            if state_key in reflected_data and "rotation" in reflected_data[state_key]:
                reflected_data[state_key]["rotation"] = -reflected_data[state_key]["rotation"]

    # Rotate rotationDegrees fields
    if reflect_rotation_degrees and "rotationTargets" in reflected_data:
        for rotation_target in reflected_data["rotationTargets"]:
            if "rotationDegrees" in rotation_target:
                rotation_target["rotationDegrees"] = -rotation_target["rotationDegrees"]

    return reflected_data


def save_json(data, output_file):
    folder_path = "paths"
    file_path = os.path.join(folder_path, output_file)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    file_name = "data.json"  # Replace with your actual JSON file name
    output_file = "reflected_data.json"  # Output file name
    ref_x, ref_y = 10, 5  # Replace with your reference points for x and y

    # User inputs for transformations
    reflect_x = input("Reflect across X-axis? (y/n): ").strip().lower() == "y"
    reflect_y = input("Reflect across Y-axis? (y/n): ").strip().lower() == "y"
    reflect_rotation = input("Reflect rotation fields? (y/n): ").strip().lower() == "y"
    reflect_rotation_degrees = input("Reflect rotationDegrees fields? (y/n): ").strip().lower() == "y"

    json_data = load_json(file_name)
    deltas = find_deltas(json_data, ref_x, ref_y)
    reflected_data = reflect_points(json_data, ref_x, ref_y, reflect_x, reflect_y, reflect_rotation,
                                    reflect_rotation_degrees)
    save_json(reflected_data, output_file)

    for entry in deltas:
        print(
            f"Point: {entry['point']}, X: {entry['x']}, Y: {entry['y']}, Delta X: {entry['delta_x']:.2f}, Delta Y: {entry['delta_y']:.2f}")
    print(f"Reflected data saved to {output_file}")