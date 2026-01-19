import json
import os

class jsonInterpreter:
    def __init__(self):
        # C:\\Users\\mayaj\\Robotics\\Reefscape\\src\\main\\deploy\\pathplanner
        self.working_directory = ""
        self.auto_names = []

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
