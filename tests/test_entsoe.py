import pytest

from dotenv import load_dotenv

import bot.entsoe as entsoe


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


test_production = {
    'Biomass': 287,
    'Fossil Brown coal/Lignite': 3392,
    'Fossil Coal-derived gas': 269,
    'Fossil Gas': 1268,
    'Fossil Hard coal': 120,
    'Fossil Oil': 0,
    'Hydro Run-of-river and poundage':180,
    'Nuclear': 2915,
    'Other renewable':264,
    'Solar': 334,
    'Waste': 19,
    'Wind Onshore': 103,
    }

@pytest.mark.skip(reason="This is calling Entsoe API")
def test_get_production():
    # Get energy for past hour from Entsoe API
    data = entsoe.request_data(entsoe.ENTSOE_URL, entsoe.ENTSOE_PARAMS)
    production = entsoe.parse_xml(data, entsoe.ENTSOE_SOURCE_MAPPING)
    assert production.keys() == test_production.keys()
    assert production['Biomass'] > 0
    assert production['Fossil Brown coal/Lignite'] > 0
    assert production['Fossil Gas'] > 0
    assert production['Nuclear'] > 0
