#!/usr/bin/env python3

import os
import datetime

import tweepy

from dotenv import load_dotenv

from bot import emojis
from bot import entsoe


load_dotenv()

def main():
    # Request electricity production data from Entsoe
    data = entsoe.request_data(entsoe.ENTSOE_URL, entsoe.ENTSOE_PARAMS)

    if data:
        production = entsoe.parse_xml(data, entsoe.ENTSOE_SOURCE_MAPPING)
        grouped_production = entsoe.group_production(production)
        reordered_production = entsoe.reorder_production(grouped_production)

        # Make a string from emojis
        percentages = emojis.calculate_percentages_better(reordered_production)
        tweet = emojis.prepare_tweet(percentages)
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
    try:
        api.update_status(status=tweet)
    except tweepy.TweepError as e:
        print(e)

if __name__ == '__main__':
    main()
