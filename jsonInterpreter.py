import json
import os

class jsonInterpreter:
    def __init__(self):
        self.working_directory = ""
        self.auto_names = []
        self.path_names = []
        self.SETTINGS_FILE = "settings.json"

    def getAutos(self):
        if self.working_directory is not None:
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
