#!/usr/bin/env python2
#-*- coding: utf-8 -*-

# Copyright (C) 2011 by Guilherme Pinto Gonçalves

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
import random

try:
    import irclib
    import ircbot
except ImportError:
    print >>sys.stderr, "This bot needs python-irclib."
    print >>sys.stderr, "http://python-irclib.sourceforge.net"

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

        self.commands = {}
        self.aliases = {}

        # Register commands
        for command_name, command_fn, aliases in commands.commands:
            self.add_command(command_name, command_fn, *aliases)

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
        command = argv[0]

        handler = self.find_command(command)
        if callable(handler):
            # Set up attributes for commands
            self.sendernick = sendernick
            self.raw_message = event.arguments()[0]

            if random.randint(1, 100) == 42:
                uprise_msg = random.choice(self.BOT_UPRISE_MSGS)
                self.connection.privmsg(self.CHANNEL, uprise_msg)

            try:
                reply = handler(self, *argv[1:])
            except TypeError:
                # Assume this was raised by wrong number of args
                return

            if reply is not None:
                reply = "%s: %s" % (sendernick, reply)
                self.connection.privmsg(self.CHANNEL, reply)

    def add_command(self, command_name, command_fn, *aliases):
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
