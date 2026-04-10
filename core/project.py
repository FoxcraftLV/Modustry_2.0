import os
import json
import shutil
from pathlib import Path
from typing import Tuple

from core.registry import registry

class Project:
	def __init__(self, path: str):
		self.path = Path(path)
		self.elements: list[Tuple[str, dict, str]] = [] # (type_id, data, sprite)
	
	def save(self, file_path: str):
		data = {
			"version": 1,
			"elements": [
				{"type": type_id, "data": data, "sprite_path":sprite}
				for type_id ,data, sprite in self.elements
				]
			}
		
		with open(file_path, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=4)
	
	def load(self, file_path: str):
		with open(file_path, "r", encoding="utf-8") as f:
			data = json.load(f)
		
		self.elements.clear()
		
		for element in data["elements"]:
			type_id: str = element["type"]
			element_data: dict = element["data"]
			sprite_path: str = element["sprite_path"]
			
			# Validate type exists
			element_cls = registry.get(type_id)
			if element_cls is None:
				print(f"Warning: Unknown element type '{type_id}' in project file.")
				continue
			
			self.elements.append((type_id, element_data, sprite_path))
	
	def create_structure(self):
		"""
		Create the full Mindustry mod folder structure.
		"""
		base = self.path
		
		folders = [
			"bundles",
			"campaign",
			"content/blocks/distribution",
			"content/blocks/drills",
			"content/blocks/effect",
			"content/blocks/environment",
			"content/blocks/liquids",
			"content/blocks/logic",
			"content/blocks/power",
			"content/blocks/production",
			"content/blocks/storage",
			"content/blocks/turrets",
			"content/blocks/units",
			"content/blocks/walls",
			"content/items",
			"content/liquids",
			"content/planets",
			"content/sectors",
			"content/status",
			"content/units",
			"content/weathers",
			"maps",
			"schematics",
			"scripts",
			"sounds",
			"sprites/blocks/distribution",
			"sprites/blocks/drills",
			"sprites/blocks/effect",
			"sprites/blocks/environment",
			"sprites/blocks/liquids",
			"sprites/blocks/logic",
			"sprites/blocks/power",
			"sprites/blocks/production",
			"sprites/blocks/storage",
			"sprites/blocks/turrets",
			"sprites/blocks/units",
			"sprites/blocks/walls",
			"sprites/items/liquids",
			"sprites/shapes",
			"sprites/status",
			"sprites/units",
			]
		
		for folder in folders:
			(base / folder).mkdir(parents=True, exist_ok=True)
	
	def write_json(self, relative_path: str, data: dict):
		"""
		Write a JSON/HJSON file inside the project.
		"""
		file_path = self.path / relative_path
		file_path.parent.mkdir(parents=True, exist_ok=True)
		
		with open(file_path, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=4)
	
	def copy_asset(self, source_path: str, target_relative: str):
		"""
		Copy an asset (image, sprite…) into the project.
		"""
		target = self.path / target_relative
		target.parent.mkdir(parents=True, exist_ok=True)
		shutil.copy(source_path, target)
	
	def write_mod_metadata(self, name, display_name, author, description, min_version, hidden):
		metadata = {
			"name": name,
			"displayName": display_name,
			"author": author,
			"description": description,
			"minGameVersion": int(min_version),
			"hidden": hidden == "true",
			}
		
		self.write_json("mod.hjson", metadata)