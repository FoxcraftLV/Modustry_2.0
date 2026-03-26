from customtkinter import *
from tkinter import filedialog
from UI.viewmodels.mod_exporter import ModExporterViewModel


def mod_window(root):
	window = CTkToplevel(root)
	window.title("Mod parameters")
	window.geometry("408x600")
	window.attributes("-topmost", True)
	
	vm = ModExporterViewModel()
	
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
	
	# Minimum Game Version
	CTkLabel(window, text="Minimum Game Version:").pack()
	CTkEntry(window, textvariable=min_version).pack()
	
	# Hidden
	CTkCheckBox(window, text="Hidden", variable=hidden, onvalue="true", offvalue="false").pack()
	
	# Progress Bar
	progress = CTkProgressBar(window, width=300)
	progress.pack(pady=20)
	
	# --- Button action ---
	def on_create():
		# Ask for folder
		path = filedialog.askdirectory(title="Select directory to save the mod")
		if not path:
			return
		
		# Create project
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
		
		# Export elements
		total = len(vm.project.elements)
		progress["maximum"] = total

		def update_progress():
			progress["value"] += 1
			window.update_idletasks()
		
		vm.export_elements(vm.project.elements, update_progress)
		
		print("Mod exported successfully!")
	
	CTkButton(window, text="Pack the mod", command=on_create).pack(pady=20)