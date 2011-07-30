import importlib

command_modules = [
    "batima",
    "bandeco",
    "fortune",
    "leave",
    "list",
    "wikipedia",
]

commands = []
for cmd in command_modules:
    mod = importlib.import_module("." + cmd, "commands")
    commands.extend(mod.command_description)
