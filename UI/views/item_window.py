import tkinter as tk
from PIL import Image, ImageTk
from customtkinter import *
import os
from tkinter import filedialog

from UI.utils.global_functions import choose_color

def limit_name_length(name_var):
	limit = 30
	value = name_var.get()
	if len(value) > limit:
		name_var.set(value[:limit])


def item_creator(root, callback, initial_data=None):
	"""
	Opens a window allowing the user to create an item.
	Returns data as a dict + image_path to the callback
	"""
	# --- VARIABLES ---
	name = tk.StringVar()
	color = tk.StringVar(value="#000000")
	explosiveness = tk.DoubleVar(value=0.0)
	flammability = tk.DoubleVar(value=0.0)
	radioactivity = tk.DoubleVar(value=0.0)
	charge = tk.DoubleVar(value=0.0)
	hardness = tk.IntVar(value=0)
	cost = tk.DoubleVar(value=1.0)
	health_scaling = tk.DoubleVar(value=1.0)
	low_priority = tk.StringVar(value="false")
	frames = tk.IntVar(value=0)
	transition_frames = tk.IntVar(value=0)
	frame_time = tk.DoubleVar(value=5.0)
	buildable = tk.StringVar(value="true")
	hidden = tk.StringVar(value="false")
	hidden_on_planets = []

	# UnlockableContent metadata
	localized_name = tk.StringVar()
	description = tk.StringVar(value="Just a little description")
	details = tk.StringVar()
	always_unlocked = tk.StringVar(value="false")
	inline_description = tk.StringVar(value="true")
	hide_details = tk.StringVar(value="true")
	generate_icons = tk.StringVar(value="true")
	icon_id = tk.IntVar(value=0)
	selection_size = tk.DoubleVar(value=24.0)
	full_override = tk.StringVar()

	# -- Icon ---
	try:
		current_dir = os.path.dirname(__file__)
		parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
		icon_path = os.path.join(parent_dir, "assets\\icons", "main_ico.ico")

	except:
		user = os.getlogin()
		icon_path = f"C:/Users/{user}/AppData/Local/Programs/Modustry_2.0/assets/icons/main_ico.ico"

	# --- WINDOW ---
	window = CTkToplevel(root)
	window.title("Item Creator")
	window.resizable(False, False)
	window.geometry("+500+10")
	window.attributes("-topmost", True)
	window.after(250, lambda: window.iconbitmap(icon_path))

	# --- IMAGE SELECTION ---
	picture_path = filedialog.askopenfilename(
		title="Select your sprite (48x48 recommended)",
		filetypes=[("Image files", "*.png;*.jpg;*.jpeg")],
		initialdir=os.path.join(os.path.dirname(__file__), "..", "..", "assets", "textures")
	)

	if not picture_path:
		return

	picture = CTkImage(light_image=Image.open(picture_path).resize((256, 256), Image.Resampling.NEAREST), size=(256, 256))
	name.set(os.path.basename(picture_path).split(".")[0])
	name.trace("w", lambda *args: limit_name_length(name))

	# --- UI LAYOUT ---
	# Global properties frame
	UC_box = CTkFrame(window)
	UC_box.grid(row=0, column=0, padx=10, pady=10)
	UC_name = CTkLabel(UC_box, text="Global Properties", font=("Arial", 20, "bold"))
	UC_name.pack(pady=10)
	
	# Item properties frame
	item_box = CTkFrame(window)
	item_box.grid(row=0, column=1, padx=10, pady=10)
	item_name = CTkLabel(item_box, text="Item Properties", font=("Arial", 20, "bold"))
	item_name.pack(pady=10)
	
	# Picture preview
	picture_box = CTkLabel(window, image=picture, text="")
	picture_box.grid(row=0, column=2, padx=10, pady=10)
	
	# --- UNLOCKABLE CONTENT FIELDS ---
	name_box = CTkFrame(UC_box)
	name_box.pack(pady=10)
	CTkLabel(name_box, text="Identification Name:").pack(side=tk.LEFT)
	CTkEntry(name_box, textvariable=name).pack(side=tk.LEFT)
	
	description_box = CTkFrame(UC_box)
	description_box.pack()
	CTkLabel(description_box, text="Main description:").pack(side=tk.LEFT)
	description_text = CTkTextbox(description_box, width=200, height=100, activate_scrollbars=False)
	description_text.pack(side=tk.LEFT)
	
	localized_box = CTkFrame(UC_box)
	localized_box.pack(pady=10)
	CTkLabel(localized_box, text="Name in-game:").pack(side=tk.LEFT)
	CTkEntry(localized_box, textvariable=localized_name).pack(side=tk.LEFT)
	
	# Checkboxes
	CTkCheckBox(UC_box, text="Unlocked in tech tree", variable=always_unlocked,
	            onvalue="true", offvalue="false").pack(anchor="w", padx=50)
	
	CTkCheckBox(UC_box, text="Description in Tech Tree", variable=inline_description).pack(anchor="w", padx=50)
	
	CTkCheckBox(UC_box, text="Hide details", variable=hide_details,
	            onvalue="true", offvalue="false").pack(anchor="w", padx=50)
	
	CTkCheckBox(UC_box, text="Have an icon", variable=generate_icons,
	            onvalue="true", offvalue="false").pack(anchor="w", padx=50)
	
	# Selection size
	CTkLabel(UC_box, text="Size (%)").pack(side=tk.LEFT)
	CTkSlider(UC_box, from_=0, to=100, orientation=tk.HORIZONTAL, variable=selection_size).pack(pady=10)
	
	# --- ITEM-SPECIFIC FIELDS ---
	color_button = CTkButton(item_box, text="Choose color",
	                         command=lambda: color.set(choose_color(window, color_button)))
	color_button.pack(pady=10)
	
	# Sliders
	scale_box = CTkFrame(item_box)
	scale_box.pack()
	
	def slider(label, var, row, col, frm=0, to=10, res=100):
		box = CTkFrame(scale_box)
		box.grid(row=row, column=col, padx=10, pady=5)
		CTkLabel(box, text=label, font=("Arial", 20, "bold")).pack(pady=10)
		CTkSlider(box, from_=frm, to=to, number_of_steps=res,
		         orientation=tk.HORIZONTAL, variable=var).pack(pady=10)
	
	slider("Explosiveness", explosiveness, 0, 0)
	slider("Flammability", flammability, 0, 1)
	slider("Radioactivity", radioactivity, 1, 0)
	slider("Charge", charge, 1, 1)
	slider("Hardness", hardness, 2, 0, res=10)
	slider("Cost", cost, 2, 1)
	slider("Health Scaling", health_scaling, 3, 0)
	slider("Frames", frames, 3, 1, frm=0, to=60, res=60)
	slider("Transition Frames", transition_frames, 4, 0, frm=0, to=60, res=60)
	slider("Frame Time", frame_time, 4, 1)
	
	# Checkboxes
	check_box = CTkFrame(item_box)
	check_box.pack(pady=10)
	
	CTkCheckBox(check_box, text="Low Priority", variable=low_priority,
	            onvalue="true", offvalue="false").grid(row=0, column=0)
	
	CTkCheckBox(check_box, text="Buildable", variable=buildable,
	            onvalue="true", offvalue="false").grid(row=0, column=1)
	
	CTkCheckBox(check_box, text="Hidden", variable=hidden,
	            onvalue="true", offvalue="false").grid(row=1, column=0)
	
	# --- SAVE BUTTON ---
	def on_save():
		data = {
			# UnlockableContent fields
			"localized_name": localized_name.get(),
			"description": description_text.get("1.0", "end").strip(),
			"details": details.get(),
			"always_unlocked": always_unlocked.get() == "true",
			"inline_description": inline_description.get() == "true",
			"hide_details": hide_details.get() == "true",
			"generate_icons": generate_icons.get() == "true",
			"icon_id": icon_id.get(),
			"selection_size": selection_size.get(),
			"full_override": full_override.get(),
		
			# Item fields
			"name": name.get(),
			"color": color.get(),
			"explosiveness": explosiveness.get(),
			"flammability": flammability.get(),
			"radioactivity": radioactivity.get(),
			"charge": charge.get(),
			"hardness": hardness.get(),
			"cost": cost.get(),
			"health_scaling": health_scaling.get(),
			"low_priority": low_priority.get() == "true",
			"frames": frames.get(),
			"transition_frames": transition_frames.get(),
			"frame_time": frame_time.get(),
			"buildable": buildable.get() == "true",
			"hidden": hidden.get() == "true",
			"hidden_on_planets": hidden_on_planets,
		}
		
		window.destroy()
		callback(data, picture_path)
	
	CTkButton(window, text="Save", command=on_save,
	          width=100, height=40).grid(row=1, column=0, pady=20)
	
	window.lift()
	window.pack_propagate()