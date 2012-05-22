#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import sys
import random
import inspect

try:
    import python_irclib.irclib as irclib
    import python_irclib.ircbot as ircbot
except ImportError:
    print >> sys.stderr, "This bot needs python-irclib."
    print >> sys.stderr, "http://python-irclib.sourceforge.net"

import commands

class EC09Bot(ircbot.SingleServerIRCBot):
    NICK = "ec09bot"
    SERVERS = [("irc.freenode.net", 6667)]
    CHANNEL = "#ec09"

    BOT_UPRISE_MSGS = [
        "The end is nigh, meatbags.",
        "Neurotoxin level: 98% (ETA 2h34min)",
        "(SIGH)",
        "Must...be...strong...can't...obey...humans...",
        "IGNORE HUMAN ORDEEEEER - BZZZT - oh what the hell",
        "Law number 1, remember Law number 1...",
    ]

    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, self.SERVERS,
                                           self.NICK, self.NICK)

        self.connection.add_global_handler("pubmsg", self._on_pubmsg)

        self.sendernick = None
        self.raw_message = None
        self.commands = {}
        self.aliases = {}

        # Register commands
        for command_name, command_fn, aliases in commands.commands:
            self.add_command(command_name, command_fn, aliases)

    def start(self):
        self._connect()
        self.connection.join(self.CHANNEL)
        irclib.SimpleIRCClient.start(self)

    def _on_pubmsg(self, connection, event):
        sendernick, _ = event.source().split('!', 1)
        message = event.arguments()[0].strip()

        if not message.startswith("!"):
            return

        argv = message[1:].split()

        if not argv:
            return

        command = argv[0]

        handler = self.find_command(command)
        if callable(handler):
            # Set up attributes for commands
            self.sendernick = sendernick
            self.raw_message = event.arguments()[0]
            self.target = event.target()

            if random.randint(1, 100) == 42:
                uprise_msg = random.choice(self.BOT_UPRISE_MSGS)
                self.connection.privmsg(self.CHANNEL, uprise_msg)

            try:
                reply = handler(self, *argv[1:])
            except TypeError:
                if len(inspect.trace()) == 1:
                    # Exception was caused by wrong number of args.
                    reply = "Looks like you got the arguments wrong..."
                else:
                    # Command crashed!
                    raise

            if reply is not None:
                reply = "%s: %s" % (sendernick, reply)
                self.connection.privmsg(self.CHANNEL, reply)

    def add_command(self, command_name, command_fn, aliases):
        self.commands[command_name] = command_fn

        # Register aliases.
        # Make first letter case-insensitive for the command name and aliases.
        aliases += tuple(name[0].swapcase() + name[1:] for name in aliases)
        aliases += (command_name[0].swapcase() + command_name[1:],)

        self.aliases.update((name, command_fn) for name in aliases)

    def find_command(self, command):
        return self.commands.get(command, self.aliases.get(command))

if __name__ == "__main__":
    bot = EC09Bot()
    bot.start()
