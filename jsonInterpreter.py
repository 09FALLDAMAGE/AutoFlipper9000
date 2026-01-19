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

    def getDefaultProjectDir(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as file:
                self.working_directory = json.load(file)["default_project_path"]
                return self.working_directory
        else:
            return ""

    def reflect_points(self, json_data, ref_x, ref_y, reflect_x=True, reflect_y=True, reflect_rotation_y=True,
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