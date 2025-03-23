# Code credit AeroAstroid github
import importlib, os, traceback
from types import *
from game import Minigame
from Minigames.add import Add

minigames_list = []
file_list = [x[:-3] for x in os.listdir("Minigames") if x.endswith(".py") and not x.startswith("__")]

for command_file in file_list:
	try:
		
		# Import file as module
		info: ModuleType = importlib.import_module("Minigames." + command_file)
		
		# Find every single class that is a subclass of the Minigame
		imported_minigames: list = []

		for cls in info.__dict__.values():
			try:
				if (issubclass(cls, Minigame)):
					if (cls.__name__ != "Minigame"):
						imported_minigames.append(cls)
			except TypeError:
				pass

		minigames_list += imported_minigames

		for minigame in imported_minigames:
			print(f"Imported {minigame.__name__} minigame from {command_file.upper()} file")

	except Exception as e: # Report commands that failed to load, and the error received

		print(f"[ERROR] Minigame from file {command_file.upper()} failed to load ({e})")
		traceback.print_exc()


def get_minigames_list() -> list:
	return minigames_list