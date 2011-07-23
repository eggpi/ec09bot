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

import time

def command_list(bot):
    bot.connection.privmsg(bot.sendernick, "Available commands (aliases):")

    # rev_commands = {callable : [command_name]}
    rev_commands = dict((fn, [cmd]) for cmd, fn in bot.commands.iteritems())

    # rev_commands = {callable : [command_name, aliases ...]}
    for alias, fn in bot.aliases.iteritems():
        rev_commands[fn].append(alias)

    # Traverse commands in alphabetical order
    for names in sorted(rev_commands.values()):
        line = names[0]
        if len(names) > 1:
            line += " (%s)" % " ".join(names[1:])

        print line
        bot.connection.privmsg(bot.sendernick, line)
        time.sleep(0.7)

command_description = [("list", command_list, ("list_commands", "ls"))]
