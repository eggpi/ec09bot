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

import datetime
import sys

try:
    import twitter
except ImportError:
    print >>sys.stderr, "This bot needs python-twitter."
    print >>sys.stderr, "http://code.google.com/p/python-twitter/"
    raise

class TweetCache(object):
    def __init__(self, account, cache_size = 100, cache_timeout = 30*60):
        self.twitter = twitter.Api()

        self.cache = []
        self.account = account
        self.cache_size = cache_size
        self.cache_timeout = cache_timeout
        self.cache_time = datetime.datetime.now()

    def get_tweets(self):
        age = (datetime.datetime.now() - self.cache_time).seconds
        if not self.cache or age > self.cache_timeout:
            self._rebuild_cache()

        if not self.cache:
            return ["Unavailable :("]

        return self.cache

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
