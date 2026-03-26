import tkinter as tk
from PIL import Image, ImageTk
from customtkinter import *

from UI.utils.global_functions import choose_color

def limit_name_length(name_var):
    limit = 30
    value = name_var.get()
    if len(value) > limit:
        name_var.set(value[:limit])


def liquid_creator(root, callback):
    """
    Opens a window allowing the user to create a liquid.
    Returns data as a dict + image_path to the callback.
    """

    # --- VARIABLES ---
    name = tk.StringVar()
    color = tk.StringVar(value="#000000")
    gas_color = tk.StringVar(value="#000000")
    bar_color = tk.StringVar(value="#000000")
    light_color = tk.StringVar(value="#000000")

    flammability = tk.DoubleVar(value=0.0)
    explosiveness = tk.DoubleVar(value=0.0)
    hidden = tk.StringVar(value="false")
    can_stay_on = []

    block_reactive = tk.StringVar(value="true")
    coolant = tk.StringVar(value="true")
    move_through_blocks = tk.StringVar(value="false")
    incinerate = tk.StringVar(value="true")

    effect = tk.StringVar(value="none")
    particle_effect = tk.StringVar(value="none")
    particle_spacing = tk.DoubleVar(value=60.0)
    boil_point = tk.DoubleVar(value=2.0)
    cap_puddles = tk.StringVar(value="true")
    vapor_effect = tk.StringVar(value="vapor")

    temperature = tk.DoubleVar(value=0.5)
    heat_capacity = tk.DoubleVar(value=0.5)
    viscosity = tk.DoubleVar(value=0.5)

    animation_frames = tk.IntVar(value=50)
    animation_scale_gas = tk.DoubleVar(value=190.0)
    animation_scale_liquid = tk.DoubleVar(value=230.0)
    gas = tk.StringVar(value="false")

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
        icon_path = os.path.join(parent_dir, "assets\icons", "main_ico.ico")

    except:
        user = os.getlogin()
        icon_path = f"C:/Users/{user}/AppData/Local/Programs/Modustry_2.0/assets/icons/main_ico.ico"

    # --- WINDOW ---
    window = CTkToplevel(root)
    window.title("Liquid Creator")
    window.resizable(False, False)
    window.geometry("+150+10")
    window.attributes("-topmost", True)
    window.after(250, lambda: window.iconbitmap(icon_path))

    # --- THEME ---
    theme = get_theme()

    # --- IMAGE SELECTION ---
    picture_path = filedialog.askopenfilename(
        title="Select your sprite (48x48 recommended)",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")],
        initialdir=os.path.join(os.path.dirname(__file__), "..", "..")
    )

    if not picture_path:
        return

    picture = ImageTk.PhotoImage(Image.open(picture_path).resize((256, 256), Image.Resampling.NEAREST), master=window)
    name.set(os.path.basename(picture_path).split(".")[0])
    name.trace("w", lambda *args: limit_name_length(name))

    # --- UI LAYOUT (unchanged) ---
    UC_box = tk.LabelFrame(window, text="Global Properties", **theme.get_frame_colors())
    UC_box.grid(row=0, column=0, padx=10, pady=10)

    liquid_box = tk.LabelFrame(window, text="Liquid Properties", **theme.get_frame_colors())
    liquid_box.grid(row=0, column=1, padx=10, pady=10)

    window._photo_image = picture
    picture_box = tk.Label(window, image=picture, **theme.get_label_colors())
    picture_box.grid(row=0, column=2, padx=10, pady=10)

    # --- UNLOCKABLE CONTENT FIELDS ---
    name_box = tk.LabelFrame(UC_box, **theme.get_frame_colors())
    name_box.pack(pady=10)
    tk.Label(name_box, text="Identification Name:", **theme.get_label_colors()).pack(side=tk.LEFT)
    tk.Entry(name_box, textvariable=name, **theme.get_entry_colors()).pack(side=tk.LEFT)

    description_box = tk.LabelFrame(UC_box, **theme.get_frame_colors())
    description_box.pack()
    tk.Label(description_box, text="Main description:", **theme.get_label_colors()).pack(side=tk.LEFT)
    description_text = tk.Text(description_box, height=5, width=20)
    description_text.pack(side=tk.LEFT)

    localized_box = tk.LabelFrame(UC_box, **theme.get_frame_colors())
    localized_box.pack(pady=10)
    tk.Label(localized_box, text="Name in-game:", **theme.get_label_colors()).pack(side=tk.LEFT)
    tk.Entry(localized_box, textvariable=localized_name, **theme.get_entry_colors()).pack(side=tk.LEFT)

    # Checkboxes
    CTkCheckBox(UC_box, text="Unlocked in tech tree", variable=always_unlocked,
                onvalue="true", offvalue="false").pack(anchor="w", padx=50)

    CTkCheckBox(UC_box, text="Description in Tech Tree", variable=inline_description).pack(anchor="w", padx=50)

    CTkCheckBox(UC_box, text="Hide details", variable=hide_details,
                onvalue="true", offvalue="false").pack(anchor="w", padx=50)

    CTkCheckBox(UC_box, text="Have an icon", variable=generate_icons,
                onvalue="true", offvalue="false").pack(anchor="w", padx=50)

    tk.Scale(UC_box, label="Size (%)", from_=0, to=100, orient=tk.HORIZONTAL,
             variable=selection_size).pack(pady=10)

    # --- LIQUID-SPECIFIC FIELDS ---
    button_frame = tk.LabelFrame(liquid_box, **theme.get_frame_colors())
    button_frame.grid(row=0, column=0, padx=10, pady=5)

    def color_btn(text, var, col):
        btn = CTkButton(button_frame, text=text,
                        command=lambda: var.set(choose_color(window, btn)),
                        width=200, height=30)
        btn.grid(row=0, column=col, padx=5, pady=5)
        return btn

    color_btn("Choose color", color, 0)
    color_btn("Gas color", gas_color, 1)
    color_btn("Bar color", bar_color, 0)
    color_btn("Light color", light_color, 1)

    # Sliders
    scale_box = tk.LabelFrame(liquid_box, **theme.get_frame_colors())
    scale_box.grid(row=1, column=0, padx=10, pady=20)

    def slider(label, var, row, col, frm=0, to=1, res=0.1):
        tk.Scale(scale_box, label=label, from_=frm, to=to, resolution=res,
                 orient=tk.HORIZONTAL, variable=var).grid(row=row, column=col, padx=10, pady=5)

    slider("Flammability", flammability, 0, 0)
    slider("Explosiveness", explosiveness, 0, 1)
    slider("Temperature", temperature, 1, 0)
    slider("Heat capacity", heat_capacity, 1, 1)
    slider("Viscosity", viscosity, 2, 0)
    slider("Particle spacing", particle_spacing, 2, 1, frm=0, to=100)
    slider("Boil point", boil_point, 3, 0, frm=0, to=100)
    slider("Animation frames", animation_frames, 3, 1, frm=0, to=100, res=1)
    slider("Animation scale gas", animation_scale_gas, 4, 0, frm=0, to=300, res=1)
    slider("Animation scale liquid", animation_scale_liquid, 4, 1, frm=0, to=300, res=1)

    # Checkboxes
    check_box = tk.LabelFrame(liquid_box, **theme.get_frame_colors())
    check_box.grid(row=0, column=1, padx=10, pady=5)

    def check(text, var):
        CTkCheckBox(check_box, text=text, variable=var,
                    onvalue="true", offvalue="false").pack(anchor="w", padx=10)

    check("Hidden", hidden)
    check("Block reactive", block_reactive)
    check("Coolant", coolant)
    check("Move through blocks", move_through_blocks)
    check("Incinerate", incinerate)
    check("Cap puddles", cap_puddles)
    check("Gas", gas)

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

            # Liquid fields
            "name": name.get(),
            "image_path": picture_path,
            "color": color.get(),
            "gas_color": gas_color.get(),
            "bar_color": bar_color.get(),
            "light_color": light_color.get(),
            "flammability": flammability.get(),
            "explosiveness": explosiveness.get(),
            "hidden": hidden.get() == "true",
            "can_stay_on": can_stay_on,
            "block_reactive": block_reactive.get() == "true",
            "coolant": coolant.get() == "true",
            "move_through_blocks": move_through_blocks.get() == "true",
            "incinerate": incinerate.get() == "true",
            "effect": effect.get(),
            "particle_effect": particle_effect.get(),
            "particle_spacing": particle_spacing.get(),
            "boil_point": boil_point.get(),
            "cap_puddles": cap_puddles.get() == "true",
            "vapor_effect": vapor_effect.get(),
            "temperature": temperature.get(),
            "heat_capacity": heat_capacity.get(),
            "viscosity": viscosity.get(),
            "animation_frames": animation_frames.get(),
            "animation_scale_gas": animation_scale_gas.get(),
            "animation_scale_liquid": animation_scale_liquid.get(),
            "gas": gas.get() == "true",
        }

        window.destroy()
        callback(data, picture_path)

    CTkButton(window, text="Save", command=on_save,
              width=100, height=40).grid(row=1, column=0, pady=20)

    window.lift()
    window.pack_propagate()
