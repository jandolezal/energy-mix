import pytest
import bot.tweet as tweet

hour_13_production = {'uhli': 3345.0, 'plyn': 1166.0, 'ropa': 0.0, 'jadro': 2829.0,
'slunce': 1498.0, 'vitr': 131.0, 'voda': 186.0, 'biomasa': 288.0, 'odpad': 18.0,
'ostatni_oze': 268.0}

hour_13_percentages = {'uhli': 34, 'plyn': 12, 'ropa': 0, 'jadro': 29,
'slunce': 15, 'vitr': 1, 'voda': 2, 'biomasa': 3, 'odpad': 0, 'ostatni_oze': 3}

hour_16_production = {'uhli': 3185.0, 'plyn': 873.0, 'ropa': 0.0, 'jadro': 2839.0,
'slunce': 1224.0, 'vitr': 159.0, 'voda': 184.0, 'biomasa': 289.0, 'odpad': 18.0,
'ostatni_oze': 269.0}

hour_16_percentages = {'uhli': 35, 'plyn': 10, 'ropa': 0, 'jadro': 31,
'slunce': 14, 'vitr': 2, 'voda': 2, 'biomasa': 3, 'odpad': 0, 'ostatni_oze': 3}


def test_calculate_percentages_13_hour():
    hour_percentages = tweet.calculate_percentages(hour_13_production)
    assert hour_percentages == hour_13_percentages

def test_calculate_percentages_16_hour():
    hour_percentages = tweet.calculate_percentages(hour_16_production)
    assert hour_percentages == hour_16_percentages
