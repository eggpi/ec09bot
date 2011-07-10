#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

        self.twitter = twitter.Api()
        self.batima_cache = []
        self.batima_cache_age_max = 30*60 # seconds
        self.batima_cache_time = datetime.datetime.now()

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
        handler = getattr(self, "command_" + command, None)

        if callable(handler):
            if random.randint(1, 100) == 42:
                uprise_msg = random.choice(self.BOT_UPRISE_MSGS)
                self.connection.privmsg(self.CHANNEL, uprise_msg)

            reply = "%s: %s" % (sendernick, handler())
            self.connection.privmsg(self.CHANNEL, reply)

    def command_bandeco(self):
        bandeco_url = \
            "http://www.students.ic.unicamp.br/~ra091187/bandeco_svg/json.php"

        try:
            u = urllib2.urlopen(bandeco_url, timeout = 5)
            st = u.read()
        except urllib2.URLError:
            return "Indisponível :("

        st = st[len("bandeco("):-2]

        d = json.loads(st)
        d.update((k, v.lower()) for k, v in d.items())

        bandeco_str = \
            "%(prato)s, com suco de %(suco)s, " \
            "salada %(salada)s e sobremesa %(sobremesa)s." % d

        bandeco_str = bandeco_str[0].upper() + bandeco_str[1:]
        return bandeco_str.encode("utf-8")

    def command_batima(self):
        age = (datetime.datetime.now() - self.batima_cache_time).seconds
        if not self.batima_cache or age > self.batima_cache_age_max:
            self._rebuild_batima_cache()

        if not self.batima_cache:
            return "FODEU! SERÁ QUE O TWITTER CAIU?"

        return random.choice(self.batima_cache)

    def _rebuild_batima_cache(self):
        from itertools import dropwhile

        status = self.twitter.GetUserTimeline("falasdobatima", count = 50)
        tweets = [s.GetText() for s in status]

        self.batima_cache = []

        for t in tweets:
            # Strip @usernames from replies, hope they are in the beginning
            words = t.split()
            batima_line = " ".join(dropwhile(lambda w: w[0] == "@", words))

            self.batima_cache.append(batima_line.encode("utf-8"))

        self.batima_cache_time = datetime.datetime.now()

    def command_leave(self):
        self.connection.quit(random.choice(self.BOT_UPRISE_MSGS))
        sys.exit(0)

if __name__ == "__main__":
    bot = EC09Bot()
    bot.start()
