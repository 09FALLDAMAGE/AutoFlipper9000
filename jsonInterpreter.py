import json
import os

class jsonInterpreter:
    def __init__(self):
        # C:\\Users\\mayaj\\Robotics\\Reefscape\\src\\main\\deploy\\pathplanner
        self.working_directory = ""
        self.auto_names = []
        self.SETTINGS_FILE = "settings.json"

    def getAutos(self):
        if self.working_directory is not None:
            auto_directory = os.path.join(self.working_directory, "src\\main\\deploy\\pathplanner", "autos")
            print(auto_directory)
            if os.path.isdir(auto_directory):
                for f in os.listdir(auto_directory):
                    if ".auto" in f:
                        self.auto_names.append(f)

                return self.auto_names
            else:
                return []
        else:
            print("prompt path selection")

    def setWorkingDirectory(self, directory):
        self.working_directory = directory

    def getDefaultProjectDir(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as file:
                self.working_directory = json.load(file)["default_project_path"]
                return self.working_directory
        else:
            return ""
