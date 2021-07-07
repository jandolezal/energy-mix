#!/usr/bin/env python3

"""The idea is to have a tweet with 100 emojis to represent the energy mix 
of electricity production in Czechia during one hour.

One emoji for each percentage share of the resource (such as coal or nuclear)
on electricity production.

Twitter counts every emoji as two characters.
"""

import csv
from pathlib import Path
from typing import List, Dict


EMOJI_MAPPING = {
    'uhli': '🏭',
    'plyn': '🔥',
    'jadro': '☢️',
    'ropa': '🛢️',
    'biomasa': '🌿',
    'voda': '💧',
    'slunce': '☀️',
    'vitr': '💨',
    'odpad': '🗑️',
    'ostatni_oze': '♻️',
}


def get_production_for_one_day(csv_path: Path) -> Dict[str, float]:
    """Get one hour of production for testing from csv file.
    Type of source in columns, 24 rows for each hour in one day.
    """

    with open(csv_path) as csvf:
        reader = csv.DictReader(csvf)
        # Convert string values to float
        one_day = [ {k: float(v) for k, v in row.items()} for row in reader]
    
    return one_day


def calculate_percentages(hour_production: Dict[str, float]) -> Dict[str, int]:
    """Calculate percentages from all values in the dictionary.

    Returns dictionary with same keys but percentage values as integers.
    Percentage total not always 100 due to rounding to integers
    """
    total = sum(float(v) for v in hour_production.values())
    percentages = {k: int(round(v/total * 100)) for k, v in hour_production.items()}
    return percentages


# https://stackoverflow.com/questions/13483430/how-to-make-rounded-percentages-add-up-to-100
# https://en.wikipedia.org/wiki/Largest_remainder_method
def calculate_percentages_better(hour_production: Dict[str, float]) -> Dict[str, int]:
    """Calculate percentages as integers from all values in the dictionary 
    using the largest remainder method.
    Returns dictionary with same keys but percentage values as integers.
    """
    total = sum(float(v) for v in hour_production.values())
    percentages = {k: (v/total * 100) for k, v in hour_production.items()}
    
    # Round down percentages and compute remainders
    floored = {k: int(v) for k, v in percentages.items()}
    remainders = {k: v1-v2 for (k, v1,), v2 in zip(percentages.items(), floored.values())}
    
    # Get difference from floored total and 100
    total_int = sum(v for v in floored.values())
    diff_total_100 = 100 - total_int

    # Distribute ones to sources with the highest remainder until total production is 100
    sorted_remainders = {
        k: v for k, v in sorted(remainders.items(),
        key=lambda remainders: remainders[1],
        reverse=True)
        }

    better_percentages = floored.copy()

    for resource in sorted_remainders:
        if diff_total_100 > 0:
            better_percentages[resource] += 1
            diff_total_100 -= 1
        else:
            break
    
    return better_percentages


def prepare_tweet(production: Dict[str, int], emoji_mapping: Dict[str, str] = EMOJI_MAPPING) -> str:
    """Produce tweet from production with maximum 10 emojis per line
    with up to 10 or 11 lines depending on the rounding to integers.
    """
    tweet_line = ''

    for resource in production:
        frequency = production.get(resource)
        symbol = emoji_mapping[resource]

        # some emojis are 2 characters long, some only one
        # set on 2 characters to make division to lines easier
        if len(symbol) == 1:  
            symbol += ' '  
        
        new_string = symbol * frequency
        tweet_line += new_string

    # 10 emojis on line, one emoji 2 characters long
    n = 20
    tweet_lines = [tweet_line[i: i+n] for i in range(0, len(tweet_line), n)]
    
    # Now that I have 10 emojis per line get rid of the whitespace
    # Twitter counts each emoji as 2 characters long no matter what
    tweet_lines = [line.replace(' ', '') for line in tweet_lines]

    tweet = '\n'.join(tweet_lines)

    return tweet


if __name__ == '__main__':
    csv_path = Path.cwd() / 'samples' /'one-april-day.csv'
    one_day = get_production_for_one_day(csv_path)
    
    # Testing what to expect
    for i in range(24):
        production = calculate_percentages(one_day[i])
        print(i)
        print(production)
        print(sum(v for v in production.values()))
        tweet = prepare_tweet(production, EMOJI_MAPPING)
        print(tweet)
        print('\n')
