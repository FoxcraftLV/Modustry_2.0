from customtkinter import *
from tkinter import filedialog

from UI.utils.global_functions import DEBUG
from UI.viewmodels.mod_exporter import ModExporterViewModel


def mod_window(root, project):
	# -- Icon ---
	try:
		current_dir = os.path.dirname(__file__)
		parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
		icon_path = os.path.join(parent_dir, "assets\\icons", "main_ico.ico")

	except FileNotFoundError:
		user = os.getlogin()
		icon_path = f"C:/Users/{user}/AppData/Local/Programs/Modustry_2.0/assets/icons/main_ico.ico"

	window = CTkToplevel(root)
	window.title("Mod parameters")
	window.geometry("408x600")
	window.attributes("-topmost", True)
	
	vm = ModExporterViewModel(project)

	# --- UI fields ---
	name = StringVar()
	display_name = StringVar()
	author = StringVar()
	min_version = StringVar()
	hidden = StringVar(value="false")
	
	# Name
	CTkLabel(window, text="Identification Name:").pack()
	CTkEntry(window, textvariable=name).pack()
	
	# Display Name
	CTkLabel(window, text="Name in-game:").pack()
	CTkEntry(window, textvariable=display_name).pack()
	
	# Author
	CTkLabel(window, text="Author:").pack()
	CTkEntry(window, textvariable=author).pack()
	
	# Description
	CTkLabel(window, text="Description:").pack()
	description_box = CTkTextbox(window, height=100)
	description_box.pack()
	description_box.insert(END, "A small description (or not)")
	
	# Minimum Game Version
	CTkLabel(window, text="Minimum Game Version:").pack()
	CTkEntry(window, textvariable=min_version).pack()
	
	# Hidden
	CTkCheckBox(window, text="Hidden", variable=hidden, onvalue="true", offvalue="false").pack()
	
	# Progress Bar
	progress = CTkProgressBar(window, width=300, orientation="horizontal")
	progress.pack(pady=20)
	progress.set(0)

	# --- Button action ---
	def on_create():
		# Ask for folder
		path = filedialog.askdirectory(title="Select directory to save the mod")
		if not path:
			return
		
		# Create export structure in the chosen folder
		vm.create_project(path)
		
		# Export metadata
		vm.export_metadata(
			name.get(),
			display_name.get(),
			author.get(),
			description_box.get("1.0", "end-1c"),
			min_version.get() or "136",
			hidden.get()
			)
		
		# Export elements from the current project
		total = len(project.elements)
		if total == 0:
			print("No elements to export!")
			return

		progress.set(0)  # Reset progress bar

		def update_progress():
			current_value = progress.get()
			progress.set(current_value + 1 / total)
			window.update_idletasks()

		if DEBUG:
			print("Exporting elements:")
			for element in project.elements:
				print(element)

		vm.export_elements(project.elements, update_progress)

		print("Mod exported successfully!")
	
	CTkButton(window, text="Pack the mod", command=on_create).pack(pady=20)