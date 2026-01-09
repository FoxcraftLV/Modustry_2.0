from core.registry import ModElement, registry
from core.base_content import UnlockableContent

class Item(ModElement):
	"""
	Declarative module representing a Mindustry item.
	Compatible with the Modustry registry system.
	"""
	
	id = "item"
	name = "Item"
	
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
		
		# Item-specific fields
		"name": str,
		"color": str, # hex string "#RRGGBB"
		"explosiveness": float,
		"flammability": float,
		"radioactivity": float,
		"charge": float,
		"hardness": int,
		"cost": float,
		"health_scaling": float,
		"low_priority": bool,
		"frames": int,
		"transition_frames": int,
		"frame_time": float,
		"buildable": bool,
		"hidden": bool,
		"hidden_on_planets": list,
	}
	
	def generate(self, data, project):
		"""
		Generates the JSON/HJSON file for this item.
		Combines UnlockableContent metadata with item-specific fields.
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
		
		metadata.update({
			"name": data["name"],
			"color": data["color"],
			"explosiveness": data["explosiveness"],
			"flammability": data["flammability"],
			"radioactivity": data["radioactivity"],
			"charge": data["charge"],
			"hardness": data["hardness"],
			"cost": data["cost"],
			"health_scaling": data["health_scaling"],
			"low_priority": data["low_priority"],
			"frames": data["frames"],
			"transition_frames": data["transition_frames"],
			"frame_time": data["frame_time"],
			"buildable": data["buildable"],
			"hidden": data["hidden"],
			"hidden_on_planets": data["hidden_on_planets"],
			})
		
		filemane = f"items/{data['name']}.json"
		project.write_json(filemane, metadata)

registry.register(Item)

class ItemStack:
	"""
	Simple utility class for representing item stacks.
	Not a ModElement.
	"""
	
	def __init__(self, item: Item, count: int):
		self.item = item
		self.count = count