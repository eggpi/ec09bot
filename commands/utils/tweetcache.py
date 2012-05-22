#-*- coding: utf-8 -*-

import datetime
import sys

try:
    import twitter
except ImportError:
    print >> sys.stderr, "----------------------------------------"
    print >> sys.stderr, "Could not import python-twitter. ",
    print >> sys.stderr, "Some commands will be disabled."
    print >> sys.stderr, "http://code.google.com/p/python-twitter/"
    print >> sys.stderr, "----------------------------------------"
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
