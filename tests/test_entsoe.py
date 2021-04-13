import pytest

from dotenv import load_dotenv

import bot.entsoe as entsoe


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


sample_production = {
    'biomasa': 1,
    'uhli_hnede': 1,
    'uhli_plyn': 1,
    'plyn': 1,
    'uhli_cerne': 1,
    'ropa': 1,
    'voda': 1,
    'jadro': 1,
    'ostatni_oze': 1,
    'slunce': 1,
    'odpad': 1,
    'vitr': 1,
    }

sample_grouped_production = {
    'biomasa': 1,
    'uhli': 3,
    'plyn': 1,
    'ropa': 1,
    'jadro': 1,
    'voda': 1,
    'slunce': 1,
    'vitr': 1,
    'odpad': 1,
    'ostatni_oze': 1,
}

@pytest.mark.skip(reason="This is calling Entsoe API")
def test_get_production():
    # Get energy for past hour from Entsoe API
    data = entsoe.request_data(entsoe.ENTSOE_URL, entsoe.ENTSOE_PARAMS)
    production = entsoe.parse_xml(data, entsoe.ENTSOE_SOURCE_MAPPING)
    assert production.keys() == sample_production.keys()
    assert production['biomasa'] > 0
    assert production['uhli_hnede'] > 0
    assert production['uhli_plyn'] > 0
    assert production['jadro'] > 0


def test_group_production():
    grouped_production = entsoe.group_production(sample_production)
    assert grouped_production == sample_grouped_production
