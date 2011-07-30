#-*- coding: utf-8 -*-

# Copyright (C) 2011 by Guilherme Pinto Gonçalves, Ivan Sichmman Freitas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
        print >>sys.stderr, "WARNING: Command %s will not work. " \
                            "Missing fortune-mod %s." % (cmdname, modname)
    else:
        command_description.append(
                [cmdname, partial(get_fortune, modname), aliases])
