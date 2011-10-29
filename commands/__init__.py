import sys
import importlib

command_modules = [
    "batima",
    "bandeco",
    "fortune",
    "leave",
    "lico",
    "list",
    "wikipedia",
    "word",
]

commands = []
for cmd in command_modules:
    try:
        mod = importlib.import_module("." + cmd, "commands")
    except ImportError:
        print >>sys.stderr, "ERROR: Failed to import %s!" % cmd
        continue

    commands.extend(mod.command_description)
