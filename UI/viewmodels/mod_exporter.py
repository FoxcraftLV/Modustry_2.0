from core.project import Project
from core.registry import registry

class ModExporterViewModel:
	def __init__(self):
		self.project = None
	
	def create_project(self, path):
		self.project = Project(path)
		self.project.create_structure()
	
	def export_metadata(self, name, display_name, author, description, min_version, hidden):
		self.project.write_mod_metadata(name, display_name, author, description, min_version, hidden)
	
	def export_elements(self, elements, progress_callback=None):
		for element_type, data in elements:
			element_cls = registry.get(element_type)
			element = element_cls()
			element.generate(data, self.project)
			
			if progress_callback:
				progress_callback()