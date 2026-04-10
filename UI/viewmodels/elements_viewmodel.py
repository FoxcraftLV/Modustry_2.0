from core.project import Project


class ElementsViewModel:
	"""
	ViewModel responsible for managing the objects inside a project.
	"""
	
	def __init__(self, project: Project):
		self.project: Project = project
	
	# Items
	def add_item(self, data, image_path):
		"""
		Add an item to the project.
		:param data: Dict of fields from the UI
		"""
		self.project.elements.append(("item", data, image_path))
		# self.project.copy_asset(image_path, f"sprites/items/{data['name']}.png")
		
	def delete_item(self, index):
		"""
		Remove an item by index.
		"""
		elements = [e for e in self.project.elements if e[0] == "item"]
		target = elements[index]
		
		# Remove from project list
		self.project.elements.remove(target)
	
	def get_items(self):
		return [e for e in self.project.elements if e[0] == "item"]
		
	# Liquids
	def add_liquid(self, data, image_path):
		"""
		Add a Liquid to the project.
		:param data: Dict of fields from the UI
		"""
		self.project.elements.append(("liquid", data, image_path))
		# self.project.copy_asset(image_path, f"sprites/items/liquids/{data['name']}.png")
	
	def delete_liquid(self, index):
		"""
		Remove a liquid by index.
		"""
		elements = [e for e in self.project.elements if e[0] == "liquid"]
		target = elements[index]
		
		# Remove from project list
		self.project.elements.remove(target)
	
	def get_liquids(self):
		return [e for e in self.project.elements if e[0] == "liquid"]