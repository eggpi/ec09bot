#-*- coding: utf-8 -*-

import threading
import collections

REENTRANT = False # try setting to True and running !lico <timeout> !lico
RUNNING = False

MINIMUM_TIMEOUT = 5
DEFAULT_TIMEOUT = 15 # seconds

DEFAULT_KEYWORD = "eunuco"

def command_lico(bot, firstarg = DEFAULT_TIMEOUT, *keyword):
    global RUNNING

    if RUNNING and not REENTRANT:
        return "Sorry, !lico already running"

    try:
        # See if we can get the timeout from the first argument
        timeout = int(firstarg)
    except ValueError:
        # Nope, treat it as part of the keyword and use the default timeout.
        keyword = (firstarg,) + keyword
        timeout = DEFAULT_TIMEOUT

    if keyword:
        keyword = " ".join(keyword)
    else:
        keyword = DEFAULT_KEYWORD

    channel = bot.channels[bot.target]
    channel.name = bot.target

    if not channel.is_oper(bot.NICK):
        return "Oops, I need to be op for that :("

    if timeout < MINIMUM_TIMEOUT:
        if timeout <= 0:
            bot.connection.kick(channel.name,
                                bot.sendernick,
                                "Funny, aren't you?")
            return
        else:
            return "Sorry, minimum timeout is " + str(MINIMUM_TIMEOUT)

    targets = collections.defaultdict(lambda: False)
    users = channel.users()

    def wait_for_keyword(connection, event):
        sendernick, _ = event.source().split('!', 1)
        message = event.arguments()[0].strip()
        if message == keyword:
            targets[sendernick] = True

    def kick_targets():
        global RUNNING

        bot.connection.remove_global_handler("pubmsg", wait_for_keyword)
        RUNNING = False

        bot.connection.privmsg(bot.CHANNEL, "Time's up!")
        for u in users:
            if u not in ("ChanServ", bot.NICK) and not targets[u]:
                bot.connection.kick(channel.name, u)

    bot.connection.add_global_handler("pubmsg", wait_for_keyword)

    RUNNING = True

    # Could also use irclib's execute_at
    timer = threading.Timer(timeout, kick_targets)
    timer.setDaemon(True)

    timer.start()

command_description = [("lico", command_lico, tuple())]
