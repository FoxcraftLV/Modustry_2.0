from customtkinter import CTkButton
from tkinter import colorchooser

DEBUG = False

def choose_color(master, widget: CTkButton):
	"""
	Open a color chooser dialog and applies the selected color to the given widget.

	:return:
		str: The selected hex color, or None.
	"""
	color = colorchooser.askcolor(parent=master, title='Choose a color')
	if color[1] is not None:
		hex_color = color[1]
		
		widget.configure(fg_color=hex_color)
		widget.configure(hover_color=darken_hex_color(hex_color, 0.2))
		
		# Adjust txt color for readability
		r, g, b = color[0]
		brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
		
		widget.configure(text_color="#000000" if brightness > 128 else "#FFFFFF")
		
		return hex_color

def darken_hex_color(hex_color: str, factor: float = 0.1):
	"""
	Darken the color by a given factor.
	"""
	if hex_color.startswith('#'):
		hex_color = hex_color[1:]
	
	r = int(hex_color[0:2], 16)
	g = int(hex_color[2:4], 16)
	b = int(hex_color[4:6], 16)
	
	r = max(0, min(255, int(r * (1 - factor))))
	g = max(0, min(255, int(g * (1 - factor))))
	b = max(0, min(255, int(b * (1 - factor))))
	
	return f'#{r:02x}{g:02x}{b:02x}'