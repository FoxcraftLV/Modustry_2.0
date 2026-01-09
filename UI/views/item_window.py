import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from customtkinter import *

from UI.utils.global_functions import choose_color


def limit_name_length(name_var):
	limit = 30
	value = name_var.get()
	if len(value) > limit:
		name_var.set(value[:limit])


def item_creator(root, callback):
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
	
	# --- IMAGE SELECTION ---
	picture_path = filedialog.askopenfilename(
		title="Select your sprite (48x48 recommended)",
		filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
		)
	
	if not picture_path:
		return
	
	picture = ImageTk.PhotoImage(Image.open(picture_path).resize((256, 256), Image.Resampling.NEAREST))
	name.set(os.path.basename(picture_path).split(".")[0])
	name.trace("w", lambda *args: limit_name_length(name))
	
	# --- WINDOW ---
	window = CTkToplevel(root)
	window.title("Item Creator")
	window.resizable(False, False)
	window.geometry("+500+10")
	window.attributes("-topmost", True)
	
	# --- UI LAYOUT ---
	dark_color_1 = "#1A1A1A"
	gray_color_1 = "#6a6a6a"
	light_blue_color = "#408ef2"
	dark_blue_color = "#2c63aa"
	hover_color = "#1f4676"
	whiteColor = "#eeeeee"
	
	# Global properties frame
	UC_box = tk.LabelFrame(window, text="Global Properties", bg=dark_color_1, fg=whiteColor)
	UC_box.grid(row=0, column=0, padx=10, pady=10)
	
	# Item properties frame
	item_box = tk.LabelFrame(window, text="Item Properties", bg=dark_color_1, fg=whiteColor)
	item_box.grid(row=0, column=1, padx=10, pady=10)
	
	# Picture preview
	picture_box = tk.Label(window, image=picture, bg=dark_color_1)
	picture_box._strong_ref_image = picture
	picture_box.grid(row=0, column=2, padx=10, pady=10)
	
	# --- UNLOCKABLE CONTENT FIELDS ---
	name_box = tk.LabelFrame(UC_box, bg=dark_color_1)
	name_box.pack(pady=10)
	tk.Label(name_box, text="Identification Name:", bg=dark_color_1, fg=whiteColor).pack(side=tk.LEFT)
	tk.Entry(name_box, textvariable=name, bg=dark_color_1, fg=whiteColor, insertbackground=whiteColor).pack(side=tk.LEFT)
	
	description_box = tk.LabelFrame(UC_box, bg=dark_color_1)
	description_box.pack()
	tk.Label(description_box, text="Main description:", bg=dark_color_1, fg=whiteColor).pack(side=tk.LEFT)
	description_text = tk.Text(description_box, height=5, width=20, bg=dark_color_1, fg=whiteColor, insertbackground=whiteColor)
	description_text.pack(side=tk.LEFT)
	
	localized_box = tk.LabelFrame(UC_box, bg=dark_color_1)
	localized_box.pack(pady=10)
	tk.Label(localized_box, text="Name in-game:", bg=dark_color_1, fg=whiteColor).pack(side=tk.LEFT)
	tk.Entry(localized_box, textvariable=localized_name, bg=dark_color_1, fg=whiteColor, insertbackground=whiteColor).pack(side=tk.LEFT)
	
	# Checkboxes
	CTkCheckBox(UC_box, text="Unlocked in tech tree", variable=always_unlocked,
	            onvalue="true", offvalue="false",
	            fg_color=dark_blue_color, bg_color=dark_color_1).pack(anchor="w", padx=50)
	
	CTkCheckBox(UC_box, text="Description in Tech Tree", variable=inline_description,
	            fg_color=dark_blue_color, bg_color=dark_color_1).pack(anchor="w", padx=50)
	
	CTkCheckBox(UC_box, text="Hide details", variable=hide_details,
	            onvalue="true", offvalue="false",
	            fg_color=dark_blue_color, bg_color=dark_color_1).pack(anchor="w", padx=50)
	
	CTkCheckBox(UC_box, text="Have an icon", variable=generate_icons,
	            onvalue="true", offvalue="false",
	            fg_color=dark_blue_color, bg_color=dark_color_1).pack(anchor="w", padx=50)
	
	# Selection size
	tk.Scale(UC_box, label="Size (%)", from_=0, to=100, orient=tk.HORIZONTAL,
	         variable=selection_size, bg=dark_color_1, fg=whiteColor).pack(pady=10)
	
	# --- ITEM-SPECIFIC FIELDS ---
	color_button = CTkButton(item_box, text="Choose color",
	                         command=lambda: color.set(choose_color(window, color_button)),
	                         fg_color=light_blue_color, hover_color=dark_blue_color)
	color_button.pack(pady=10)
	
	# Sliders
	scale_box = tk.LabelFrame(item_box, bg=dark_color_1)
	scale_box.pack()
	
	def slider(label, var, row, col, frm=0, to=10, res=0.1):
		tk.Scale(scale_box, label=label, from_=frm, to=to, resolution=res,
		         orient=tk.HORIZONTAL, variable=var,
		         bg=dark_color_1, fg=whiteColor).grid(row=row, column=col, padx=10, pady=5)
	
	slider("Explosiveness", explosiveness, 0, 0)
	slider("Flammability", flammability, 0, 1)
	slider("Radioactivity", radioactivity, 1, 0)
	slider("Charge", charge, 1, 1)
	slider("Hardness", hardness, 2, 0, res=1)
	slider("Cost", cost, 2, 1)
	slider("Health Scaling", health_scaling, 3, 0)
	slider("Frames", frames, 3, 1, frm=0, to=60, res=1)
	slider("Transition Frames", transition_frames, 4, 0, frm=0, to=60, res=1)
	slider("Frame Time", frame_time, 4, 1)
	
	# Checkboxes
	check_box = tk.LabelFrame(item_box, bg=dark_color_1)
	check_box.pack(pady=10)
	
	CTkCheckBox(check_box, text="Low Priority", variable=low_priority,
	            onvalue="true", offvalue="false",
	            fg_color=dark_blue_color, bg_color=dark_color_1).grid(row=0, column=0)
	
	CTkCheckBox(check_box, text="Buildable", variable=buildable,
	            onvalue="true", offvalue="false",
	            fg_color=dark_blue_color, bg_color=dark_color_1).grid(row=0, column=1)
	
	CTkCheckBox(check_box, text="Hidden", variable=hidden,
	            onvalue="true", offvalue="false",
	            fg_color=dark_blue_color, bg_color=dark_color_1).grid(row=1, column=0)
	
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
	          fg_color=light_blue_color, hover_color=dark_blue_color,
	          width=100, height=40).grid(row=1, column=0, pady=20)
	
	window.lift()
	window.pack_propagate()