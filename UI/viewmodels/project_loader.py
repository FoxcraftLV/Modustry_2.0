from tkinter import filedialog
from core.project import Project


class ProjectLoaderViewModel:
	def __init__(self, project: Project):
		self.project = project
	
	def save_project(self):
		file_path = filedialog.asksaveasfilename(
			defaultextension=".modustry",
			filetypes=[("Modustry Project", "*.modustry"), ("All files", "*.*")],
			title="Save Project"
		)
		if not file_path:
			return
		
		self.project.save(file_path)
		print(f"Project saved to {file_path} successfully.")
		
	def load_project(self):
		file_path = filedialog.askopenfilename(
			filetypes=[("Modustry Project", "*.modustry"), ("All files", "*.*")],
			title="Load Project"
			)
		if not file_path:
			return
		
		self.project.load(file_path)
		print(f"Project loaded from {file_path} successfully.")