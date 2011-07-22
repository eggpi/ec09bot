#-*- coding: utf-8 -*-

# Copyright (C) 2011 by Guilherme Pinto Gonçalves, Ivan Sichmann Freitas

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

import itertools

def command_list(bot):
    # Chain all command names and aliases together
    commands_and_aliases = itertools.chain(bot.commands, bot.aliases)

    # Group them by the callable they map to
    grouped = itertools.groupby(
                      sorted(commands_and_aliases, key = bot.find_command),
                      bot.find_command)

    # And sort by command name
    grouped_names = sorted(list(g) for k, g in grouped)

    bot.connection.privmsg(bot.sendernick, "Available commands (aliases):")
    for names in grouped_names:
    	line = names[0]
    	if len(names) > 1:
    		line += " (%s)" % " ".join(names[1:])

    	bot.connection.privmsg(bot.sendernick, line)

command_description = [("list", command_list, ("list_commands", "ls"))]
