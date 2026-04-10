import tkinter as tk
from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk
import os
import json

from UI.viewmodels.elements_viewmodel import ElementsViewModel
from UI.viewmodels.project_loader import ProjectLoaderViewModel
from UI.viewmodels.mod_exporter import ModExporterViewModel


class MainWindow:
	def __init__(self, root, project, data, icon_path):
		self.root = root
		self.project = project
		self.data = data
		self.icon_path = icon_path

		# ViewModels
		self.elements_vm = ElementsViewModel(project)
		self.loader_vm = ProjectLoaderViewModel(project)
		self.export_vm = ModExporterViewModel()

		self.root.title("Modustry")
		self.root.state("zoomed")
		self.root.resizable(True, True)

		try:
			current_dir = os.path.dirname(__file__)
			parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
			icon_path = os.path.join(parent_dir, "assets\\icons", "main_ico.ico")

		except:
			user = os.getlogin()
			icon_path = f"C:/Users/{user}/AppData/Local/Programs/Modustry_2.0/assets/icons/main_ico.ico"

		self.root.after(250, lambda: self.root.iconbitmap(icon_path))
		
		# --- MENU ---
		root_bar = tk.Menu(self.root, font=CTkFont(size=10))

		# -- File --
		file_menu = tk.Menu(root_bar, tearoff=0, font=CTkFont(size=10))
		file_menu.add_command(label="Save project", command=self.loader_vm.save_project)
		file_menu.add_command(label="Load project", command=lambda: self._load_project())
		file_menu.add_command(label="Pack", command=lambda: self._open_export_window())

		# -- Help --
		help_menu = tk.Menu(root_bar, tearoff=0, font=CTkFont(size=10))

		# Doc
		doc_menu = tk.Menu(help_menu, tearoff=0, font=CTkFont(size=10))
		doc_menu.add_command(label="Items", command=self._open_items_docs)
		doc_menu.add_command(label="Liquids", command=self._open_liquids_docs)
		doc_menu.add_command(label="UI", command=self._open_ui_docs)
		doc_menu.add_command(label="Export", command=self._open_export_docs)

		# -- Edit --
		edit_menu = tk.Menu(root_bar, tearoff=0, font=CTkFont(size=10))

		# Mode
		mode = tk.Menu(edit_menu, tearoff=0, font=CTkFont(size=10))
		mode.add_command(label="Light", command=self._set_light)
		mode.add_command(label="Dark", command=self._set_dark)
		edit_menu.add_cascade(label="Mode", menu=mode)

		# Theme
		theme = tk.Menu(edit_menu, tearoff=0, font=CTkFont(size=10))
		theme.add_command(label="Modustry", command=self._set_modustry)
		theme.add_command(label="Cryofluid", command=self._set_cryofluid)
		theme.add_command(label="Hazard", command=self._set_hazard)
		theme.add_command(label="Standard", command=self._set_standard)
		theme.add_command(label="Contrast", command=self._set_contrast)
		edit_menu.add_cascade(label="Theme", menu=theme)


		root_bar.add_cascade(label="File", menu=file_menu)
		root_bar.add_cascade(label="Edit", menu=edit_menu)
		root_bar.add_cascade(label="Help", menu=help_menu)

		help_menu.add_cascade(label="Documentation", menu=doc_menu)

		self.root.config(menu=root_bar)

		# Main frame
		self.main_frame = CTkFrame(self.root)
		self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)
		
		# Tabs
		self.tabs = CTkTabview(self.main_frame)
		self.tabs.pack(fill="both", expand=True)
		
		# ADDING TABS
		self.items_tab = self.tabs.add("Items")
		self.liquids_tab = self.tabs.add("Liquids")
		
		# Build UI
		self._build_items_ui()
		self._build_liquids_ui()
		
		# Initial refresh
		self.refresh_lists()
	
	# --- DOCUMENTATION ---
	def _open_items_docs(self):
		from UI.views.documentation_window import DocumentationWindow
		DocumentationWindow(self.root, "./docs/items.md")
	
	def _open_liquids_docs(self):
		from UI.views.documentation_window import DocumentationWindow
		DocumentationWindow(self.root, "./docs/liquids.md")
	
	def _open_ui_docs(self):
		from UI.views.documentation_window import DocumentationWindow
		DocumentationWindow(self.root, "./docs/ui.md")
	
	def _open_export_docs(self):
		from UI.views.documentation_window import DocumentationWindow
		DocumentationWindow(self.root, "./docs/export.md")
	
	# --- UI BUILDERS ---
	def _build_items_ui(self):
		self.item_bin_buttons = []
		self.items_labels = []
		self.items_images = []
		
		self.items_frame = CTkFrame(self.items_tab, border_width=2)
		self.items_frame.pack(side="left", padx=10, pady=10)
		
		CTkLabel(self.items_frame, text="Items", font=("Arial", 30, "bold")).pack(pady=5)
		
		CTkButton(self.items_frame, text="Add Item",
		          command=self._add_item,
		          width=120, height=40,
		          font=CTkFont(size=18)).pack(padx=23, pady=(20, 10), anchor="w")

		self.item_scrollable_frame = CTkScrollableFrame(self.items_frame, width=400, height=650)
		self.item_scrollable_frame.pack(padx=(23, 23), pady=(0, 23), fill="both", expand=True)
	
	def _build_liquids_ui(self):
		self.liquid_bin_buttons = []
		self.liquid_labels = []
		self.liquid_images = []

		self.liquids_frame = CTkFrame(self.liquids_tab, border_width=2)
		self.liquids_frame.pack(side="left", padx=10, pady=10)
		
		CTkLabel(self.liquids_frame, text="Liquids", font=("Arial", 30, "bold")).pack(pady=5)
		
		CTkButton(self.liquids_frame, text="Add Liquid",
		          command=self._add_liquid,
		          width=120, height=40,
		          font=CTkFont(size=18)).pack(padx=23, pady=(20, 10), anchor="w")

		self.liquids_scrollable_frame = CTkScrollableFrame(self.liquids_frame, width=400, height=650)
		self.liquids_scrollable_frame.pack(padx=(23, 23), pady=(0, 23), fill="both", expand=True)
	
	# --- ACTIONS ---

	# Add
	def _add_item(self):
		from UI.views.item_window import item_creator
		item_creator(self.root, self._on_item_created)

	def _add_liquid(self):
		from UI.views.liquid_window import liquid_creator
		liquid_creator(self.root, self._on_liquid_created)

	# Created
	def _on_item_created(self, data, image_path):
		self.elements_vm.add_item(data, image_path)
		self.refresh_lists()

	def _on_liquid_created(self, data, image_path):
		self.elements_vm.add_liquid(data, image_path)
		self.refresh_lists()

	# File
	def _load_project(self):
		self.loader_vm.load_project()
		self.refresh_lists()
	
	def _open_export_window(self):
		from UI.views.mod_window import mod_window
		mod_window(self.root, self.project)

	def restart_app(self):
		python = sys.executable
		os.execl(python, python, * sys.argv)

	# -- Preferences --
	# Mode
	def _set_light(self):
		self.data["mode"] = "light"
		set_appearance_mode("light")
		with open("assets\\settings\\preferences.json", "w") as file:
			json.dump(self.data, file)

	def _set_dark(self):
		self.data["mode"] = "dark"
		set_appearance_mode("dark")
		with open("assets\\settings\\preferences.json", "w") as file:
			json.dump(self.data, file)

	# Theme
	def _set_modustry(self):
		self.data["theme"] = "modustry-theme"
		set_default_color_theme(f"assets\\themes\\modustry-theme.json")
		with open("assets\\settings\\preferences.json", "w") as file:
			json.dump(self.data, file)
		self.restart_app()

	def _set_cryofluid(self):
		self.data["theme"] = "mindustry-cryofluid"
		set_default_color_theme(f"assets\\themes\\mindustry-cryofluid.json")
		with open("assets\\settings\\preferences.json", "w") as file:
			json.dump(self.data, file)
		self.restart_app()

	def _set_hazard(self):
		self.data["theme"] = "mindustry-hazard"
		set_default_color_theme(f"assets\\themes\\mindustry-hazard.json")
		with open("assets\\settings\\preferences.json", "w") as file:
			json.dump(self.data, file)
		self.restart_app()

	def _set_standard(self):
		self.data["theme"] = "mindustry-standard"
		set_default_color_theme(f"assets\\themes\\mindustry-standard.json")
		with open("assets\\settings\\preferences.json", "w") as file:
			json.dump(self.data, file)
		self.restart_app()

	def _set_contrast(self):
		self.data["theme"] = "mindustry-contrast+"
		set_default_color_theme(f"assets\\themes\\mindustry-contrast+.json")
		with open("assets\\settings\\preferences.json", "w") as file:
			json.dump(self.data, file)
		self.restart_app()

	
	# --- LIST REFRESH ---
	def refresh_lists(self):
		items = self.elements_vm.get_items()
		liquids = self.elements_vm.get_liquids()
		
		self._refresh_items(items)
		self._refresh_liquids(liquids)
	
	def _refresh_items(self, items):
		# Clear old widgets
		for w in self.item_scrollable_frame.winfo_children():
			w.destroy()
		
		self.items_images = []
		
		for i, (_, data, img_path) in enumerate(items):
			if os.path.exists(img_path):
				img = CTkImage(Image.open(img_path).resize((50, 50), Image.Resampling.NEAREST), size=(50, 50))
			else:
				img = None
			
			label_img = CTkLabel(self.item_scrollable_frame, image=img, text="")
			label_img.grid(row=i, column=0)
			self.items_images.append(img)
			
			label_text = CTkLabel(self.item_scrollable_frame, text=data['name'], font=CTkFont(size=18))
			label_text.grid(row=i, column=1, padx=10, pady=5)
			
			delete_btn = CTkButton(self.item_scrollable_frame,
			                       command=lambda index=i: self._delete_item(index),
			                       width=20, height=20,
			                       text="X")
			delete_btn.grid(row=i, column=2, padx=5)

	def _refresh_liquids(self, liquids):
		for w in self.liquids_scrollable_frame.winfo_children():
			w.destroy()

		self.liquid_images = []

		for i, (_, data, img_path) in enumerate(liquids):
			if os.path.exists(img_path):
				img = ImageTk.PhotoImage(Image.open(img_path).resize((50, 50)))
			else:
				img = None

			label_img = CTkLabel(self.liquids_scrollable_frame, image=img, text="")
			label_img.grid(row=i, column=0)
			self.liquid_images.append(img)

			label_text = CTkLabel(self.liquids_scrollable_frame, text=data["name"], font=CTkFont(size=18))
			label_text.grid(row=i, column=1, padx=10, pady=5)

			delete_btn = CTkButton(self.liquids_scrollable_frame,
								   command=lambda index=i: self._delete_liquid(index),
								   width=20, height=20,
								   text="X")
			delete_btn.grid(row=i, column=2, padx=5)

	# --- DELETE ACTIONS ---
	def _delete_item(self, index):
		if messagebox.askyesno("Delete item", "Are you sure"):
			self.elements_vm.delete_item(index)
			self.refresh_lists()

	def _delete_liquid(self, index):
		if messagebox.askyesno("Delete liquid", "Are you sure"):
			self.elements_vm.delete_liquid(index)
			self.refresh_lists()