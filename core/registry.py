
class ModElement:
	id = None
	name = None
	fields = {}
	
	def generate(self, data, project):
		raise NotImplementedError


class ModRegistry:
	def __init__(self):
		self._elements = {}
		
	def register(self, element_cls):
		self._elements[element_cls.id] = element_cls
	
	def get(self, element_id):
		return self._elements.get(element_id)

registry = ModRegistry()