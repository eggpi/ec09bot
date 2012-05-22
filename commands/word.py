#-*- coding: utf-8 -*-

import re
import urllib2

def command_word(bot, lang = "english"):
    if lang == "english":
        url = "http://merriam-webster.com/word-of-the-day/"

        try:
            content = urllib2.urlopen(url, timeout = 5).read()
        except:
            return "Failed to grab page!"

        word = re.findall(r'"main_entry_word">([^<]+)<', content)[0]
        function = re.findall(r'"word_function">([^<]+)', content)[0]
        definitions = re.findall(r'<span class="ssens"><strong>:</strong>'
                                 r' *([^<]+)</span>', content)

        bot.connection.privmsg(bot.CHANNEL, "%s (%s)" % (word, function))
        for defnum, definition in enumerate(definitions):
            bot.connection.privmsg(bot.CHANNEL, "%d: %s" % (defnum, definition))
        bot.connection.privmsg(bot.CHANNEL, url)

    else:
        return "Unrecognized language!"

command_description = [("word", command_word, ("dailyword", "wordoftheday"))]
