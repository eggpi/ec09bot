#-*- coding: utf-8 -*-

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

        bot.connection.privmsg(bot.sendernick, line)
        time.sleep(0.7)

command_description = [("list", command_list, ("list_commands", "ls"))]
