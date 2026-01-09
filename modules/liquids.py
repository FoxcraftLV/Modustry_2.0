from core.registry import ModElement, registry
from core.base_content import UnlockableContent


class Liquid(ModElement):
	"""
	Declarative module representing a Mindustry liquid.
	Compatible with the Modustry registry system.
	"""
	id = "liquid"
	name = "Liquid"
	
	# Fields exposed to the UI
	fields = {
		# UnlockableContent metadata
		"localized_name": str,
		"description": str,
		"details": str,
		"always_unlocked": bool,
		"inline_description": bool,
		"hide_details": bool,
		"generate_icons": bool,
		"icon_id": int,
		"selection_size": float,
		"full_override": str,
		
		# Liquid-specific fields
		"name": str,
		"image_path": str,
		"color": str,
		"gas_color": str,
		"bar_color": str,
		"light_color": str,
		"flammability": float,
		"explosiveness": float,
		"hidden": bool,
		"can_stay_on": list,
		"block_reactive": bool,
		"coolant": bool,
		"move_through_blocks": bool,
		"incinerate": bool,
		"effect": str,
		"particle_effect": str,
		"particle_spacing": float,
		"boil_point": float,
		"cap_puddles": bool,
		"vapor_effect": str,
		"temperature": float,
		"heat_capacity": float,
		"viscosity": float,
		"animation_frames": int,
		"animation_scale_gas": float,
		"animation_scale_liquid": float,
		"gas": bool,
		}
	
	def generate(self, data, project):
		"""
		Generate the JSON/HJSON file for this liquid.
		Combines UnlockableContent metadata with liquid-specifics fields.
		"""
		
		# Convert UnlockableContent metadata
		metadata = UnlockableContent(
			localized_name=data["localized_name"],
			description=data["description"],
			details=data["details"],
			always_unlocked=data["always_unlocked"],
			inline_description=data["inline_description"],
			hide_details=data["hide_details"],
			generate_icons=data["generate_icons"],
			icon_id=data["icon_id"],
			selection_size=data["selection_size"],
			full_override=data["full_override"],
			).to_dict()
		
		# Merge liquid-specific fields
		metadata.update({
			"name": data["name"],
			"image_path": data["image_path"],
			"color": data["color"],
			"gas_color": data["gas_color"],
			"bar_color": data["bar_color"],
			"light_color": data["light_color"],
			"flammability": data["flammability"],
			"explosiveness": data["explosiveness"],
			"hidden": data["hidden"],
			"can_stay_on": data["can_stay_on"],
			"block_reactive": data["block_reactive"],
			"coolant": data["coolant"],
			"move_through_blocks": data["move_through_blocks"],
			"incinerate": data["incinerate"],
			"effect": data["effect"],
			"particle_effect": data["particle_effect"],
			"particle_spacing": data["particle_spacing"],
			"boil_point": data["boil_point"],
			"cap_puddles": data["cap_puddles"],
			"vapor_effect": data["vapor_effect"],
			"temperature": data["temperature"],
			"heat_capacity": data["heat_capacity"],
			"viscosity": data["viscosity"],
			"animation_frames": data["animation_frames"],
			"animation_scale_gas": data["animation_scale_gas"],
			"animation_scale_liquid": data["animation_scale_liquid"],
			"gas": data["gas"],
			})
		
		# Write the file
		filename = f"{data['name']}.json"
		project.write_json_metadata(filename, metadata)


# Register the Liquid module
registry.register(Liquid)


class LiquidStack:
	def __init__(self, liquid: Liquid, amount: float):
		self.liquid = liquid
		self.amount = amount