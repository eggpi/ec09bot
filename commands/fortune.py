#-*- coding: utf-8 -*-

import sys
import subprocess
from functools import partial

def get_installed_fortunes():
    try:
        proc = subprocess.Popen(("/usr/bin/fortune", "-f"),
                                stderr = subprocess.PIPE)
    except OSError:
        return set()

    return set(line.split()[1] for line in proc.stderr)

def get_fortune(fortunemod, bot):
    try:
        proc = subprocess.Popen(("/usr/bin/fortune", "-a", fortunemod),
                                stderr = subprocess.PIPE,
                                stdout = subprocess.PIPE)
    except OSError:
        return "no fortune here!"

    if proc.wait() == 0:
        for line in proc.stdout:
            bot.connection.privmsg(bot.CHANNEL, line.lstrip())
    else:
        return "fortune failed: " + proc.stderr.read()

# (module_name, command_name, command_aliases)
fortunes = [
    ("bofh-excuses", "bofh", ("bastard", "operator")),
    ("calvin", "calvin", tuple()),
    ("chucknorris", "chuck", ("chucknorris", "chuckfact")),
    ("computers", "comp", tuple()),
    ("futurama", "futurama", tuple()),
    ("the-godfather", "godfather", tuple()),
    ("homer", "homer", tuple()),
    ("kernelcookies", "kernel", tuple()),
    ("linux", "linux", tuple()),
    ("literature", "literature", tuple()),
    ("matrix", "matrix", tuple()),
    ("montypython", "montypython", tuple()),
    ("southpark", "southpark", tuple()),
    ("startrek", "startrek", tuple()),
    ("starwars", "starwars", ("sw", "usetheforce")),
    ("wisdom", "wisdom", tuple()),
]

command_description = []
installed_mods = get_installed_fortunes()

for modname, cmdname, aliases in fortunes:
    if modname not in installed_mods:
        print >> sys.stderr, "WARNING: Command %s will not work. " \
                            "Missing fortune-mod %s." % (cmdname, modname)
    else:
        command_description.append(
                [cmdname, partial(get_fortune, modname), aliases])
