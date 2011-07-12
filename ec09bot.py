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
import json
import random
import urllib2
import datetime

try:
    import irclib
    import ircbot
except ImportError:
    print >>sys.stderr, "This bot needs python-irclib."
    print >>sys.stderr, "http://python-irclib.sourceforge.net"

try:
    import twitter
except ImportError:
    print >>sys.stderr, "This bot needs python-twitter."
    print >>sys.stderr, "http://code.google.com/p/python-twitter/"

class TwitterCommand(object):
    """ Fetches a random tweet from a twitter account. """

    def __init__(self, account, cache_size = 100, cache_timeout = 30*60):
        self.twitter = twitter.Api()

        self.cache = []
        self.account = account
        self.cache_size = cache_size
        self.cache_timeout = cache_timeout
        self.cache_time = datetime.datetime.now()

    def __call__(self):
        age = (datetime.datetime.now() - self.cache_time).seconds
        if not self.cache or age > self.cache_timeout:
            self._rebuild_cache()

        if not self.cache:
            return "Unavailable :("

        return random.choice(self.cache)

    def _rebuild_cache(self):
        from itertools import dropwhile

        try:
            status = self.twitter.GetUserTimeline(self.account,
                                                  count = self.cache_size)
        except twitter.TwitterError:
            return

        tweets = [s.GetText() for s in status]

        self.cache = []
        for t in tweets:
            # Strip @usernames from replies, hope they are in the beginning
            words = t.split()
            text = " ".join(dropwhile(lambda w: w[0] == "@", words))

            self.cache.append(text.encode("utf-8"))

        self.cache_time = datetime.datetime.now()

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

        # Register commands
        self.commands = {}
        self.add_command("leave", self.command_leave)
        self.add_command("bandeco", self.command_bandeco)
        self.add_command("batima", TwitterCommand("falasdobatima"), "bátima")
        self.add_command("chuck", TwitterCommand("dailychuckfact"),
                         "chucknorris")

    def start(self):
        self._connect()
        self.connection.join(self.CHANNEL)
        irclib.SimpleIRCClient.start(self)

    def _on_pubmsg(self, connection, event):
        sendernick, _ = event.source().split('!', 1)
        message = event.arguments()[0].strip()

        if not message.startswith("!"):
            return

        command = message[1:]
        handler = self.commands.get(command)

        if callable(handler):
            if random.randint(1, 100) == 42:
                uprise_msg = random.choice(self.BOT_UPRISE_MSGS)
                self.connection.privmsg(self.CHANNEL, uprise_msg)

            reply = "%s: %s" % (sendernick, handler())
            self.connection.privmsg(self.CHANNEL, reply)

    def add_command(self, command_name, command_fn, *aliases):
        # Make first letter case-insensitive
        all_names = (command_name,) + aliases
        all_names += tuple(name[0].swapcase() + name[1:] for name in all_names)

        self.commands.update((name, command_fn) for name in all_names)

    def command_bandeco(self):
        bandeco_url = \
            "http://www.students.ic.unicamp.br/~ra091187/bandeco_svg/json.php"

        try:
            u = urllib2.urlopen(bandeco_url, timeout = 5)
            st = u.read()
        except urllib2.URLError:
            return "Indisponível :("

        st = st[len("bandeco("):-2]

        d = json.loads(st, encoding = "latin-1")
        d.update((k, v.strip().lower()) for k, v in d.items())

        bandeco_str = \
            "%(prato)s, com suco de %(suco)s, " \
            "salada %(salada)s e sobremesa %(sobremesa)s." % d

        bandeco_str = bandeco_str[0].upper() + bandeco_str[1:]
        return bandeco_str.encode("utf-8")

    def command_leave(self):
        self.connection.quit(random.choice(self.BOT_UPRISE_MSGS))
        sys.exit(0)

if __name__ == "__main__":
    bot = EC09Bot()
    bot.start()
