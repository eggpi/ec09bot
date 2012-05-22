#-*- coding: utf-8 -*-

import random
from utils import tweetcache

tweets = tweetcache.TweetCache("falasdobatima")

def command_batima(bot):
    return random.choice(tweets.get_tweets())

command_description = [("batima", command_batima, ("bátima",))]
