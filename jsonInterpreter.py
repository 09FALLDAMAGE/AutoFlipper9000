import json
import os

class jsonInterpreter:
    def __init__(self):
        self.working_directory = ""
        self.auto_names = []
        self.path_names = []
        self.SETTINGS_FILE = "settings.json"
        self.ref_x, self.ref_y = 8.77, 4.03

    def getAutos(self):
        if self.working_directory is not None:
            self.auto_names = []
            auto_directory = os.path.join(self.working_directory, "src\\main\\deploy\\pathplanner", "autos")
            if os.path.isdir(auto_directory):
                for f in os.listdir(auto_directory):
                    if ".auto" in f:
                        self.auto_names.append(f)

                return self.auto_names
            else:
                return []
        else:
            return []

    def getPaths(self):
        if self.working_directory is not None:

            self.path_names = []

            path_directory = os.path.join(self.working_directory, "src\\main\\deploy\\pathplanner", "paths")
            if os.path.isdir(path_directory):
                for f in os.listdir(path_directory):
                    if ".path" in f:
                        self.path_names.append(f)

                return self.path_names
            else:
                return []
        else:
            return []

    def setWorkingDirectory(self, directory):
        self.working_directory = directory
        settings = {"default_project_path": directory}
        with open(self.SETTINGS_FILE, 'w') as file:
            json.dump(settings, file, indent=4)

    def save_auto(self, data, output_file):
        folder_path = "src\\main\\deploy\\pathplanner\\autos"
        file_path = os.path.join(self.working_directory, folder_path, output_file)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def getDefaultProjectDir(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as file:
                self.working_directory = json.load(file)["default_project_path"]
                return self.working_directory
        else:
            return ""

    def find_deltas(self, json_data, ref_x, ref_y):
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

    def save_json(self, data, output_file):
        folder_path = "src\\main\\deploy\\pathplanner\\paths"
        file_path = os.path.join(self.working_directory, folder_path, output_file)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def extract_path_names(self, command_data):
        path_names = set()
        if isinstance(command_data, dict):
            if "type" in command_data and command_data["type"] == "path" and "data" in command_data and "pathName" in \
                    command_data["data"]:
                path_names.add(command_data["data"]["pathName"])
            for key, value in command_data.items():
                path_names.update(self.extract_path_names(value))
        elif isinstance(command_data, list):
            for item in command_data:
                path_names.update(self.extract_path_names(item))
        return path_names

    def load_json(self, file_name):
        folder_path = "src\\main\\deploy\\pathplanner\\paths"  # Folder where JSON files are stored
        file_path = os.path.join(self.working_directory, folder_path, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def flip(self, auto_name, flip_auto_name, reflect_x=True, reflect_y=True, reflect_rotation_y=True,
                   reflect_rotation_x=True, path_prefix = ""):
        with open(os.path.join(self.working_directory, "src\\main\\deploy\\pathplanner\\autos", auto_name), 'r') as file:
            command_data = json.load(file)

        flipped_commands = command_data.copy()

        path_names = self.extract_path_names(command_data)
        for path_name in path_names:
            file_name = f"{path_name}.path"
            output_file = f"{path_prefix}{path_name}.path"

            if os.path.exists(os.path.join(self.working_directory, "src\\main\\deploy\\pathplanner\\paths", file_name)):
                json_data = self.load_json(file_name)
                deltas = self.find_deltas(json_data, self.ref_x, self.ref_y)
                reflected_data = self.reflect_points(json_data, self.ref_x, self.ref_y, reflect_x, reflect_y, reflect_rotation_x, reflect_rotation_y)

                self.save_json(reflected_data, output_file)

                for entry in deltas:
                    print(
                        f"Point: {entry['point']}, X: {entry['x']}, Y: {entry['y']}, Delta X: {entry['delta_x']:.2f}, Delta Y: {entry['delta_y']:.2f}")
                print(f"Reflected data saved to {output_file}")

                def update_command_paths(data):
                    if isinstance(data, dict):
                        if "type" in data and data["type"] == "path" and "data" in data and "pathName" in data["data"]:
                            if data["data"]["pathName"] in path_names:
                                data["data"]["pathName"] = f"{path_prefix}{data['data']['pathName']}"
                        for key, value in data.items():
                            update_command_paths(value)
                    elif isinstance(data, list):
                        for item in data:
                            update_command_paths(item)

                update_command_paths(flipped_commands)
            else:
                print(f"File {file_name} not found in paths folder.")

        flipped_commands_file = f"{auto_name}.auto"
        self.save_auto(flipped_commands, flipped_commands_file)
        print(f"Flipped commands file saved to {flipped_commands_file}")

    def reflect_points(self, json_data, ref_x, ref_y, reflect_x=True, reflect_y=True, reflect_rotation_x=True,
                   reflect_rotation_y=True):
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