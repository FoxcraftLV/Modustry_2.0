import tkinter as tk
from idlelib.outwin import file_line_pats
from tkinter import messagebox, filedialog
from customtkinter import *
from PIL import Image, ImageTk
import os

from UI.viewmodels.elements_viewmodel import ElementsViewModel
from UI.viewmodels.project_loader import ProjectLoaderViewModel
from UI.viewmodels.mod_exporter import ModExporterViewModel


class MainWindow:
	def __init__(self, root, project):
		self.root = root
		self.project = project
		
		# ViewModels
		self.elements_vm = ElementsViewModel(project)
		self.loader_vm = ProjectLoaderViewModel(project)
		self.export_vm = ModExporterViewModel()
		
		# UI colors
		self.dark_color_1 = "#1A1A1A"
		self.gray_color_1 = "#6A6A6A"
		self.light_blue_color = "#408EF2"
		self.dark_blue_color = "#2c63AA"
		self.white_color ="#FFFFFF"
		
		self.root.title("Modustry")
		self.root.state("zoomed")
		self.root.resizable(True, True)
		set_appearance_mode("dark")
		
		# Icon
		try:
			current_dir = os.path.dirname(__file__)
			parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
			icon_path = os.path.join(parent_dir, "assets\icons", "main_icon.ico")
			
		except:
			user = os.getlogin()
			icon_path = f"C:/Users/{user}/AppData/Local/Programs/Modustry_2.0/assets/icons/main_icon.png"
		
		self.root.after(250, lambda: self.root.iconbitmap(icon_path))
		
		# Menu
		root_bar = tk.Menu(self.root, font=CTkFont(size=16))
		
		file_menu = tk.Menu(root_bar, tearoff=0, font=CTkFont(size=16))
		file_menu.add_command(label="Save project", command=self.loader_vm.save_project)
		file_menu.add_command(label="Load project", command=lambda: self._load_project())
		file_menu.add_command(label="Pack", command=lambda: self._open_export_window())
		
		root_bar.add_cascade(label="File", menu=file_menu)
		self.root.config(menu=root_bar)
		
		# Main frame
		self.main_frame = CTkFrame(self.root)
		self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)
		
		# Build UI
		self._build_items_ui()
		self._build_liquids_ui()
		
		# Initial refresh
		self.refresh_lists()
		
	# --- UI BUILDERS ---
	def _build_items_ui(self):
		self.item_bin_buttons = []
		self.items_labels = []
		self.items_images = []
		
		self.items_frame = CTkFrame(self.main_frame, fg_color=self.dark_color_1,
		                            border_color=self.white_color, border_width=2)
		self.items_frame.pack(side="left", padx=10, pady=10)
		
		CTkLabel(self.items_frame, text="Items", bg_color=self.dark_color_1,
		         text_color=self.white_color, font=("Arial", 30, "underline")).pack(pady=5)
		
		CTkButton(self.items_frame, text="Add Item",
		          command=self._add_item,
		          width=120, height=40,
		          fg_color=self.light_blue_color,
		          hover_color=self.dark_blue_color,
		          text_color=self.dark_color_1,
		          font=CTkFont(size=18)).pack(padx=23, pady=(20, 18), anchor="w")
		
		# Container
		self.item_container = CTkFrame(self.items_frame, fg_color=self.dark_color_1)
		self.item_container.pack(padx=(23, 0), pady=(0, 23), fill="both", expand=True)
		
		# Canvas
		self.item_canvas = tk.Canvas(self.item_container, width=400, height=650,
		                             background=self.dark_color_1,
		                             highlightbackground=self.gray_color_1)
		self.item_canvas.pack(side="left", fill="both", expand=True)
		
		# Scrollbar
		self.item_scrollbar = CTkScrollbar(self.item_container, orientation="vertical",
		                                   command=self.item_canvas.yview, width=15)
		self.item_scrollbar.pack(side="right", fill="y")
		
		# Scrollable frame
		self.item_scrollable_frame = tk.Frame(self.item_canvas, background=self.dark_color_1)
		self.item_scrollable_frame.bind(
			"<Configure>",
			lambda e: self.item_canvas.configure(scrollregion=self.item_canvas.bbox("all"))
			)
		
		self.item_canvas.create_window((0, 0), window=self.item_scrollable_frame, anchor="nw")
		self.item_canvas.configure(yscrollcommand=self.item_scrollbar.set)
	
	
	def _build_liquids_ui(self):
		self.liquid_bin_buttons = []
		self.liquid_labels = []
		self.liquid_images = []
		
		self.liquids_frame = CTkFrame(self.main_frame, fg_color=self.dark_color_1,
		                              border_color=self.white_color, border_width=2)
		self.liquids_frame.pack(side="right", padx=10, pady=10)
		
		CTkLabel(self.liquids_frame, text="Liquids", bg_color=self.dark_color_1,
		         text_color=self.white_color, font=("Arial", 30, "underline")).pack(pady=5)
		
		CTkButton(self.liquids_frame, text="Add Liquid",
		          command=self._add_liquid,
		          width=120, height=40,
		          fg_color=self.light_blue_color,
		          hover_color=self.dark_blue_color,
		          text_color=self.dark_color_1,
		          font=CTkFont(size=18)).pack(padx=23, pady=(20, 10), anchor="w")
		
		# Container
		self.liquid_container = CTkFrame(self.liquids_frame, fg_color=self.dark_color_1)
		self.liquid_container.pack(padx=(23, 0), pady=(0, 23), fill="both", expand=True)
		
		# Canvas
		self.liquids_canvas = tk.Canvas(self.liquid_container, width=400, height=650,
		                                background=self.dark_color_1,
		                                highlightbackground=self.gray_color_1)
		self.liquids_canvas.pack(side="left", fill="both", expand=True)
		
		# Scrollbar
		self.liquids_scrollbar = CTkScrollbar(self.liquid_container, orientation="vertical",
		                                      command=self.liquids_canvas.yview, width=15)
		self.liquids_scrollbar.pack(side="right", fill="y")
		
		# Scrollable frame
		self.liquids_scrollable_frame = tk.Frame(self.liquids_canvas, background=self.dark_color_1)
		self.liquids_scrollable_frame.bind(
			"<Configure>",
			lambda e: self.liquids_canvas.configure(scrollregion=self.liquids_canvas.bbox("all"))
			)
		
		self.liquids_canvas.create_window((0, 0), window=self.liquids_scrollable_frame, anchor="nw")
		self.liquids_canvas.configure(yscrollcommand=self.liquids_scrollbar.set)
	
	# --- ACTIONS ---
	def _add_item(self):
		from UI.views.item_window import item_creator
		item_creator(self.root, self._on_item_created)
	
	def _on_item_created(self, data, image_path):
		self.elements_vm.add_item(data, image_path)
		self.refresh_lists()
	
	def _add_liquid(self):
		from UI.views.liquid_window import liquid_creator
		liquid_creator(self.root, self._on_liquid_created)
	
	def _on_liquid_created(self, data, image_path):
		self.elements_vm.add_liquid(data, image_path)
		self.refresh_lists()
	
	def _load_project(self):
		self.loader_vm.load_project()
		self.refresh_lists()
	
	def _open_export_window(self):
		from UI.views.mod_window import mod_window
		mod_window(self.root)
	
	
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
		
		for i, (_, data) in enumerate(items):
			img_path = f"{self.project.path}/sprites/items/{data['name']}.png"
			if os.path.exists(img_path):
				img = ImageTk.PhotoImage(Image.open(img_path).resize((50, 50)))
			else:
				img = None
			
			label_img = tk.Label(self.item_scrollable_frame, image=img, bg=self.dark_color_1)
			label_img.grid(row=i, column=0)
			self.items_images.append(img)
			
			label_text = tk.Label(self.item_scrollable_frame, text=data['name'],
			                      bg=self.dark_color_1, fg=self.white_color,
			                      font=CTkFont(size=18))
			label_text.grid(row=i, column=1, padx=10, pady=5)
			
			delete_btn = CTkButton(self.item_scrollable_frame,
			                       command=lambda index=i: self._delete_item(index),
			                       width=20, height=20,
			                       text="X",
			                       fg_color=self.light_blue_color,
			                       hover_color=self.dark_blue_color)
			delete_btn.grid(row=i, column=2, padx=5)
	
	def _delete_item(self, index):
		if messagebox.askyesno("Delete item", "Are you sure"):
			self.elements_vm.delete_item(index)
			self.refresh_lists()
	
	def _refresh_liquids(self, liquids):
		for w in self.liquids_scrollable_frame.winfo_children():
			w.destroy()
		
		self.liquid_images = []
		
		for i, (_, data) in enumerate(liquids):
			img_path = f"{self.project.path}/sprites/items/liquids/{data['name']}.png"
			if os.path.exists(img_path):
				img = ImageTk.PhotoImage(Image.open(img_path).resize((50, 50)))
			else:
				img = None
		
			label_img = tk.Label(self.liquids_scrollable_frame, image=img, bg=self.dark_color_1)
			label_img.grid(row=i, column=0)
			self.liquid_images.append(img)
			
			label_text = tk.Label(self.liquids_scrollable_frame, text=data["name"],
			                      bg=self.dark_color_1, fg=self.white_color,
			                      font=CTkFont(size=18))
			label_text.grid(row=i, column=1, padx=10, pady=5)
			
			delete_btn = CTkButton(self.liquids_scrollable_frame,
			                       command=lambda index=i: self._delete_liquid(index),
			                       width=20, height=20,
			                       text="X",
			                       fg_color=self.light_blue_color,
			                       hover_color=self.dark_blue_color)
			delete_btn.grid(row=i, column=2, padx=5)
		
	def _delete_liquid(self, index):
		if messagebox.askyesno("Delete liquid", "Are you sure"):
			self.elements_vm.delete_liquid(index)
			self.refresh_lists()