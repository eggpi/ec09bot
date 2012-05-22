#-*- coding: utf-8 -*-

import sys
import random

def command_leave(bot):
    bot.connection.quit(random.choice(bot.BOT_UPRISE_MSGS))
    sys.exit(0)

command_description = [("leave", command_leave, tuple())]
