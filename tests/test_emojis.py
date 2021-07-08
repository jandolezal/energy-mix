import pytest

import bot.emojis as emojis


def test_calculate_percentages_13_hour():
    hour_13_production = {'uhli': 3345.0, 'plyn': 1166.0, 'ropa': 0.0, 'jadro': 2829.0,
    'slunce': 1498.0, 'vitr': 131.0, 'voda': 186.0, 'biomasa': 288.0, 'odpad': 18.0,
    'ostatni_oze': 268.0}

    hour_13_percentages = {'uhli': 34, 'plyn': 12, 'ropa': 0, 'jadro': 29,
    'slunce': 15, 'vitr': 1, 'voda': 2, 'biomasa': 3, 'odpad': 0, 'ostatni_oze': 3}

    hour_percentages = emojis.calculate_percentages(hour_13_production)
    assert hour_percentages == hour_13_percentages


def test_calculate_percentages_16_hour():
    hour_16_production = {'uhli': 3185.0, 'plyn': 873.0, 'ropa': 0.0, 'jadro': 2839.0,
    'slunce': 1224.0, 'vitr': 159.0, 'voda': 184.0, 'biomasa': 289.0, 'odpad': 18.0,
    'ostatni_oze': 269.0}

    hour_16_percentages = {'uhli': 35, 'plyn': 10, 'ropa': 0, 'jadro': 31,
    'slunce': 14, 'vitr': 2, 'voda': 2, 'biomasa': 3, 'odpad': 0, 'ostatni_oze': 3}

    hour_percentages = emojis.calculate_percentages(hour_16_production)
    assert hour_percentages == hour_16_percentages


# Case with 98 total when rounding percentages to integers
# See end of samples/entsoe.ipynb
def test_calculate_percentages_better_18_hour():
    hour_18_production = {'uhli': 3465.0, 'plyn': 1263.0, 'ropa': 0.0, 'jadro': 2853.0,
    'slunce': 295.0, 'vitr': 134.0, 'voda': 185.0, 'biomasa': 293.0, 'odpad': 18.0,
    'ostatni_oze': 279.0}

    hour_18_percentages = {'uhli': 40, 'plyn': 14, 'ropa': 0, 'jadro': 33,
    'slunce': 3, 'vitr': 2, 'voda': 2, 'biomasa': 3, 'odpad': 0, 'ostatni_oze': 3}

    hour_percentages = emojis.calculate_percentages_better(hour_18_production)
    assert hour_percentages == hour_18_percentages


def test_prepare_tweet_18_hour():
    hour_18_percentages = {
        'uhli': 40, 'plyn': 14, 'ropa': 0, 'jadro': 33, 'slunce': 3, 'vitr': 2,
        'voda': 2, 'biomasa': 3, 'odpad': 0, 'ostatni_oze': 3
        }
    
    tweet = (
        '🏭🏭🏭🏭🏭🏭🏭🏭🏭🏭\n'
        '🏭🏭🏭🏭🏭🏭🏭🏭🏭🏭\n'
        '🏭🏭🏭🏭🏭🏭🏭🏭🏭🏭\n'
        '🏭🏭🏭🏭🏭🏭🏭🏭🏭🏭\n'
        '🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥\n'
        '🔥🔥🔥🔥☢️☢️☢️☢️☢️☢️\n'
        '☢️☢️☢️☢️☢️☢️☢️☢️☢️☢️\n'
        '☢️☢️☢️☢️☢️☢️☢️☢️☢️☢️\n'
        '☢️☢️☢️☢️☢️☢️☢️☀️☀️☀️\n'
        '💨💨💧💧🌿🌿🌿♻️♻️♻️'
    )

    assert tweet == emojis.prepare_tweet(production=hour_18_percentages)


# Case with 99 total when rounding percentages to whole numbers
def test_calculate_percentages_better_12_hour():
    hour_12_production = {'uhli': 3345.0, 'plyn': 1166.0, 'ropa': 0.0, 'jadro': 2829.0,
    'slunce': 1498.0, 'vitr': 131.0, 'voda': 186.0, 'biomasa': 288.0, 'odpad': 18.0,
    'ostatni_oze': 268.0}

    hour_12_percentages = {'uhli': 34, 'plyn': 12, 'ropa': 0, 'jadro': 29,
    'slunce': 16, 'vitr': 1, 'voda': 2, 'biomasa': 3, 'odpad': 0, 'ostatni_oze': 3}

    hour_percentages = emojis.calculate_percentages_better(hour_12_production)
    assert hour_percentages == hour_12_percentages


# Case with 100 total when rounding percentages to whole numbers
def test_calculate_percentages_better_7_hour():
    hour_7_production = {'uhli': 3807.0, 'plyn': 1326.0, 'ropa': 0.0, 'jadro': 2801.0,
    'slunce': 17.0, 'vitr': 146.0, 'voda': 182.0, 'biomasa': 279.0, 'odpad': 17.0,
    'ostatni_oze': 275.0}

    hour_7_percentages = {'uhli': 43, 'plyn': 15, 'ropa': 0, 'jadro': 32,
    'slunce': 0, 'vitr': 2, 'voda': 2, 'biomasa': 3, 'odpad': 0, 'ostatni_oze': 3}

    hour_percentages = emojis.calculate_percentages_better(hour_7_production)
    assert hour_percentages == hour_7_percentages


# Case with 101 total when rounding percentages to whole numbers
def test_calculate_percentages_better_8_hour():
    hour_8_production = {'uhli': 3832.0, 'plyn': 1337.0, 'ropa': 0.0, 'jadro': 2823.0,
    'slunce': 229.0, 'vitr': 149.0, 'voda': 177.0, 'biomasa': 282.0, 'odpad': 18.0,
    'ostatni_oze': 266.0}

    hour_8_percentages = {'uhli': 42, 'plyn': 15, 'ropa': 0, 'jadro': 31,
    'slunce': 2, 'vitr': 2, 'voda': 2, 'biomasa': 3, 'odpad': 0, 'ostatni_oze': 3}

    hour_percentages = emojis.calculate_percentages_better(hour_8_production)
    assert hour_percentages == hour_8_percentages


def test_prepare_tweet_8_hour():
    hour_8_percentages = {
        'uhli': 42, 'plyn': 15, 'ropa': 0, 'jadro': 31, 'slunce': 2, 'vitr': 2,
        'voda': 2, 'biomasa': 3, 'odpad': 0, 'ostatni_oze': 3,
        }
    
    tweet = (
        '🏭🏭🏭🏭🏭🏭🏭🏭🏭🏭\n'
        '🏭🏭🏭🏭🏭🏭🏭🏭🏭🏭\n'
        '🏭🏭🏭🏭🏭🏭🏭🏭🏭🏭\n'
        '🏭🏭🏭🏭🏭🏭🏭🏭🏭🏭\n'
        '🏭🏭🔥🔥🔥🔥🔥🔥🔥🔥\n'
        '🔥🔥🔥🔥🔥🔥🔥☢️☢️☢️\n'
        '☢️☢️☢️☢️☢️☢️☢️☢️☢️☢️\n'
        '☢️☢️☢️☢️☢️☢️☢️☢️☢️☢️\n'
        '☢️☢️☢️☢️☢️☢️☢️☢️☀️☀️\n'
        '💨💨💧💧🌿🌿🌿♻️♻️♻️'
    )

    assert tweet == emojis.prepare_tweet(production=hour_8_percentages)
