#!/usr/bin/env python3

import os
import datetime

from dotenv import load_dotenv
import tweepy

from bot import emojis
from bot import entsoe


load_dotenv()

def main():
    # Request electricity production data from Entsoe for past hour
    data = entsoe.get_data()

    if data:
        # Make a string from emojis based on data
        percentages = emojis.calculate_percentages_better(data)
        tweet = emojis.prepare_tweet(production=percentages)
    else:
        raise SystemExit

    # Twitter app authentication and setup
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # Tweet the emoji string
    api.update_status(status=tweet)


if __name__ == '__main__':
    main()
