#!/usr/bin/env python3

import os
import datetime

import tweepy

from entsoe import url, params, res_map, request_data, parse_xml, data_check
from dotenv import load_dotenv
from tweet import calculate_percentages, prepare_tweet


load_dotenv()


if data_check(energy):
    # Twitter app authentication
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Tweet the data
    production = tweet.calculate_percentages(hour_production)
    tweet = tweet.prepare_tweet(production)
    # api.update_status(status=tweet)
