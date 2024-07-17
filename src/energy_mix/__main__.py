#!/usr/bin/env python3

import logging
import os

from dotenv import load_dotenv
import tweepy  # type: ignore

from . import emojis
from . import entsoe


load_dotenv()


def main():
    # Request electricity production data from Entsoe for past hour
    data = entsoe.get_data()

    if data:
        # Make a string from emojis based on data
        percentages = emojis.calculate_percentages_better(data)
        tweet = emojis.prepare_tweet(production=percentages)
    else:
        raise SystemExit

    # Twitter app authentication and setup
    # https://docs.tweepy.org/en/stable/examples.html
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    # Tweet the emoji string
    try:
        client.create_tweet(text=tweet)
    except tweepy.errors.Forbidden as e:
        logging.error(e)
        raise SystemExit


if __name__ == "__main__":
    main()
