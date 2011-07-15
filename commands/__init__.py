import sys
import importlib

sys.path.append("commands")

command_modules = [
"batima",
"bandeco",
"chuck",
"leave",
]

commands = []
for cmd in command_modules:
	mod = importlib.import_module(cmd, "commands")
	commands.extend(mod.command_description)
