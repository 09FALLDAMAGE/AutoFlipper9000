import customtkinter
from customtkinter import filedialog
import os
from jsonInterpreter import jsonInterpreter
import webbrowser

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.backend = jsonInterpreter()

        self.title("Auto Flipper 9000")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Auto Flipper\n9000", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.folder_input_label = customtkinter.CTkLabel(self.sidebar_frame, text="Current project:", anchor="w")
        self.folder_input_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        if self.backend.getDefaultProjectDir() != "":

            self.project_label = customtkinter.CTkLabel(self.sidebar_frame, text=os.path.basename(self.backend.getDefaultProjectDir()), anchor="w", text_color="orange")
            if len(self.backend.getPaths()) > 0:
                self.project_label.configure(text_color="#17e321")
        else:
            self.project_label = customtkinter.CTkLabel(self.sidebar_frame, text="Not Selected", anchor="w", text_color="red")

        self.project_label.grid(row=2, column=0, padx=20, pady=(50, 0))


        self.folder_input_button = customtkinter.CTkButton(self.sidebar_frame, text="Open Project",
                                                           command=self.open_file_dialog_event)
        self.folder_input_button.grid(row=3, column=0, padx=20, pady=(10, 0))

        self.x_switch = customtkinter.CTkSwitch(master=self.sidebar_frame, text="Flip x")
        self.x_switch.grid(row=4, column=0, padx=10, pady=(60, 0))

        self.y_switch = customtkinter.CTkSwitch(master=self.sidebar_frame, text="Flip y")
        self.y_switch.grid(row=4, column=0, padx=10, pady=(110, 0))

        self.x_rotation_switch = customtkinter.CTkSwitch(master=self.sidebar_frame, text="Flip Rotation x")
        self.x_rotation_switch.grid(row=4, column=0, padx=10, pady=(160, 0))

        self.y_rotation_switch = customtkinter.CTkSwitch(master=self.sidebar_frame, text="Flip Rotation y")
        self.y_rotation_switch.grid(row=4, column=0, padx=10, pady=(210, 0))

        self.flipper_9000_inator = customtkinter.CTkButton(self.sidebar_frame, text="Flip!",
                                                   command=self.flip)
        self.flipper_9000_inator.grid(row=4, column=0, padx=20, pady=(0, 0))


        self.help_button = customtkinter.CTkButton(self.sidebar_frame, text="Documentation",
                                                           command=self.open_docs)
        self.help_button.grid(row=5, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(0, 0))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["System", "Dark", "Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=7, column=0, padx=20, pady=(10, 20))


        # create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, rowspan = 3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Autos")
        self.tabview.add("Paths")
        self.tabview.tab("Autos").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Autos").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Paths").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Paths").grid_rowconfigure(0, weight=1)


        self.auto_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Autos"))
        self.auto_scrollable_frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.auto_scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.auton_widgets = []

        self.path_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Paths"))
        self.path_scrollable_frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.path_scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.path_widgets = []

        if len(self.backend.getAutos()) > 0:
            iterator = 0
            for auto in self.backend.getAutos():
                switch = customtkinter.CTkSwitch(master=self.auto_scrollable_frame, text=f"{auto}")
                switch.grid(row=int(iterator / 3), column=int(iterator % 3), padx=10, pady=(0, 20))
                self.auton_widgets.append(switch)
                iterator += 1
        else:
            self.project_label.configure(text_color="orange")
            self.no_autos_label = customtkinter.CTkLabel(self.auto_scrollable_frame, text="No Autos\n \nLoad the base folder\nof your robot project",
                                                     font=customtkinter.CTkFont(size=20, weight="bold"))
            self.no_autos_label.grid(row=0, column=1, padx=10, pady=(20, 10))
            self.auton_widgets.append(self.no_autos_label)

        if len(self.backend.getPaths()) > 0:
            iterator = 0
            for auto in self.backend.getPaths():
                switch = customtkinter.CTkSwitch(master=self.path_scrollable_frame, text=f"{auto}")
                switch.grid(row=int(iterator / 3), column=int(iterator % 3), padx=10, pady=(0, 20))
                self.path_widgets.append(switch)
                iterator += 1
        else:
            self.project_label.configure(text_color="orange")
            self.no_paths_label = customtkinter.CTkLabel(self.path_scrollable_frame, text="No Paths\n \nLoad the base folder\nof your robot project",
                                                     font=customtkinter.CTkFont(size=20, weight="bold"))
            self.no_paths_label.grid(row=0, column=1, padx=10, pady=(20, 10))
            self.path_widgets.append(self.no_paths_label)

        self.searchbar = customtkinter.CTkEntry(self, placeholder_text="Press Enter To Search")
        self.searchbar.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.searchbar.bind('<Return>', self.search_items)
        self.searchbar.bind('<Escape>', self.clear_search)


    def open_file_dialog_event(self):
        path = customtkinter.filedialog.askdirectory()
        self.project_label.configure(text=os.path.basename(path), text_color="#17e321")
        self.backend.setWorkingDirectory(path)
        self.refresh_tabs_event()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def refresh_tabs_event(self):
        if len(self.backend.getAutos()) > 0:
            for widget in self.auton_widgets:
                widget.destroy()

            self.auton_widgets = []

            iterator = 0
            for auto in self.backend.getAutos():
                switch = customtkinter.CTkSwitch(master=self.auto_scrollable_frame, text=f"{auto}")
                switch.grid(row=int(iterator / 3), column=int(iterator % 3), padx=10, pady=(0, 20))
                self.auton_widgets.append(switch)
                iterator += 1
        else:
            self.project_label.configure(text_color="orange")
            for widget in self.auton_widgets:
                widget.destroy()

            self.auton_widgets = []

            self.no_autos_label = customtkinter.CTkLabel(self.auto_scrollable_frame, text="No Autos\n \nLoad the base folder\nof your robot project",
                                                     font=customtkinter.CTkFont(size=20, weight="bold"))
            self.no_autos_label.grid(row=0, column=1, padx=10, pady=(20, 10))
            self.auton_widgets.append(self.no_autos_label)

        if len(self.backend.getPaths()) > 0:
            for widget in self.path_widgets:
                widget.destroy()

            self.path_widgets = []
            iterator = 0
            for path in self.backend.getPaths():
                switch = customtkinter.CTkSwitch(master=self.path_scrollable_frame, text=f"{path}")
                switch.grid(row=int(iterator / 3), column=int(iterator % 3), padx=10, pady=(0, 20))
                self.path_widgets.append(switch)
                iterator += 1
        else:
            self.project_label.configure(text_color="orange")
            for widget in self.path_widgets:
                widget.destroy()

            self.path_widgets = []

            self.no_paths_label = customtkinter.CTkLabel(self.path_scrollable_frame, text="No Paths\n \nLoad the base folder\nof your robot project",
                                                     font=customtkinter.CTkFont(size=20, weight="bold"))
            self.no_paths_label.grid(row=0, column=1, padx=10, pady=(20, 10))
            self.path_widgets.append(self.no_paths_label)


    def clear_search(self, entry):
        self.searchbar.delete(0, len(self.searchbar.get()))
        self.search_items(None)

    def search_items(self, event):
        tab = self.tabview.get()
        term = self.searchbar.get()

        tab = tab == "Autos"

        if tab:
            if len(self.backend.getAutos()) > 0:
                for widget in self.auton_widgets:
                    widget.destroy()

                self.auton_widgets = []
                iterator = 0
                for auto in self.backend.getAutos():
                    if term.lower() in auto.lower():
                        switch = customtkinter.CTkSwitch(master=self.auto_scrollable_frame, text=f"{auto}")
                        switch.grid(row=int(iterator / 3), column=int(iterator % 3), padx=10, pady=(0, 20))
                        self.auton_widgets.append(switch)
                        iterator += 1
        else:
            if len(self.backend.getPaths()) > 0:
                for widget in self.path_widgets:
                    widget.destroy()

                self.path_widgets = []
                iterator = 0
                for path in self.backend.getPaths():
                    if term.lower() in path.lower():
                        switch = customtkinter.CTkSwitch(master=self.path_scrollable_frame, text=f"{path}")
                        switch.grid(row=int(iterator / 3), column=int(iterator % 3), padx=10, pady=(0, 20))
                        self.path_widgets.append(switch)
                        iterator += 1

    def open_docs(self):
        webbrowser.open("https://github.com/09FALLDAMAGE/AutoFlipper9000/blob/main/README.md")

    def flip(self):
        flipx = self.x_switch.get()
        flipy = self.y_switch.get()
        fliprotx = self.x_rotation_switch.get()
        fliproty = self.y_rotation_switch.get()
        if self.tabview.get() == "Autos":
            if True: # single auto
                auto_name_entry = customtkinter.CTkInputDialog(text="What should the name of the new auto be?",
                                                         title="Flipping, 30%")
                auto_name = auto_name_entry.get_input()
                if auto_name is None or auto_name == "":
                    return

                path_prefix_entry = customtkinter.CTkInputDialog(text="Enter new path prefix", title="Flipping, 60%")
                path_prefix = path_prefix_entry.get_input()
                if path_prefix is None or path_prefix == "":
                    return

                # command_name_entry = customtkinter.CTkInputDialog(text="Enter new command file prefix", title="Flipping, 90%")
                # command_name = command_name_entry.get_input()
                # if command_name is None or command_name == "":
                #     return

                self.backend.flip("autoname",flipx, flipy, fliprotx, fliproty, path_prefix)

            elif False: # multiple autos
                auto_name = customtkinter.CTkInputDialog(
                    text="You are flipping multiple autos\nEnter a prefix for the new autos", title="Flipping, 30%")
                print(auto_name.get_input())
                path_prefix = customtkinter.CTkInputDialog(text="Enter new path prefix", title="Flipping, 60%")
                command_name = customtkinter.CTkInputDialog(text="Enter new command file prefix", title="Flipping, 90%")

            else: # no autos
                return








if __name__ == "__main__":
    app = App()
    app.mainloop()