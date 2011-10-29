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

import threading
import collections

DEFAULT_TIMEOUT = 5 # seconds
DEFAULT_KEYWORD = "eunuco"

def command_lico(bot, timeout = DEFAULT_TIMEOUT, keyword = DEFAULT_KEYWORD):
    try:
        timeout = int(timeout)
    except ValueError:
        return "Invalid timeout"

    channel = bot.channels[bot.target]
    channel.name = bot.target

    if not channel.is_oper(bot.NICK):
        return "Oops, I need to be op for that :("

    targets = collections.defaultdict(lambda: False)
    users = channel.users()

    def wait_for_keyword(connection, event):
        sendernick, _ = event.source().split('!', 1)
        message = event.arguments()[0].strip()
        if message == keyword:
            targets[sendernick] = True

    def kick_targets():
        bot.connection.remove_global_handler("pubmsg", wait_for_keyword)

        for u in users:
            if u not in ("ChanServ", bot.NICK) and not targets[u]:
                bot.connection.kick(channel.name, u)

    bot.connection.add_global_handler("pubmsg", wait_for_keyword)

    # Could also use irclib's execute_at
    timer = threading.Timer(timeout, kick_targets)
    timer.setDaemon(True)

    timer.start()

command_description = [("lico", command_lico, tuple())]
