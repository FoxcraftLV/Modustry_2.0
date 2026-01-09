from customtkinter import CTk
from core.project import Project
from UI.views.main_window import MainWindow


def main():
	# Create the main Tkinter window
	root = CTk()
	
	# Create an empty project (no path yet
	# The user will choose a folder when exporting or saving
	project = Project(path=".")
	
	#Create the main UI windows
	app = MainWindow(root, project)
	
	# Start the UI loop
	root.mainloop()


if __name__ == "__main__":
	main()