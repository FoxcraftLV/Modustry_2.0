class UnlockableContent:
	"""
	Base class for any Mindustry content that can be unlocked.
	This class does not generate files by itself; it's only stores metadata.
	"""
	
	def __init__(
			self,
			localized_name: str,
			description: str,
			details: str,
			always_unlocked: bool = False,
			inline_description: str = False,
			hide_details: bool = False,
			generate_icons: bool = True,
			icon_id: int = 0,
			selection_size: float = 1.0,
			full_override: str = ""
			):

		self.localized_name = localized_name
		self.description = description
		self.details = details
		
		self.always_unlocked = always_unlocked
		self.inline_description = inline_description
		self.hide_details = hide_details
		
		self.generate_icons = generate_icons
		self.icon_id = icon_id
		self.selection_size = selection_size
		
		self.full_override = full_override
	
	def to_dict(self):
		"""
		Convert this content metadata to a dictionary.
		Useful for JSON/HJSON generation.
		"""
		return {
			"localizedName": self.localized_name,
			"description": self.description,
			"details": self.details,
			"alwaysUnlocked": self.always_unlocked,
			"inlineDescription": self.inline_description,
			"hideDetails": self.hide_details,
			"generateIcons": self.generate_icons,
			"iconId": self.icon_id,
			"selectionSize": self.selection_size,
			"fullOverride": self.full_override
		}