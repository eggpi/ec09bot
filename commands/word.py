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
