from customtkinter import CTk, set_default_color_theme, set_appearance_mode
import json
import os

from core.project import Project
from UI.views.main_window import MainWindow
import modules


def main():

	# Icon path
	try:
		current_dir = os.path.dirname(__file__)
		parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
		icon_path = os.path.join(parent_dir, "assets/icons", "main_ico.ico")

	except:
		user = os.getlogin()
		icon_path = f"C:/Users/{user}/AppData/Local/Programs/Modustry_2.0/assets/icons/main_ico.ico"


	# apply theme
	with open("assets/settings/preferences.json") as file:
		data = json.load(file)
	set_appearance_mode(data["mode"])
	set_default_color_theme(f"assets/themes/{data["theme"]}.json")

	# Create the main Tkinter window
	root = CTk()
	
	# Create an empty project (no path yet
	# The user will choose a folder when exporting or saving
	project = Project(path=".")
	
	#Create the main UI windows
	app = MainWindow(root, project, data, icon_path)
	
	# Start the UI loop
	root.mainloop()


if __name__ == "__main__":
	main()