import datetime

import pytest
from dotenv import load_dotenv

import energy_mix.entsoe as entsoe


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
    'voda_rezervoar': 1,
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
    'voda': 2,
    'slunce': 1,
    'vitr': 1,
    'odpad': 1,
    'ostatni_oze': 1,
}

sample_reordered_production = {
    'uhli': 3,
    'voda': 2,
    'plyn': 1,
    'ropa': 1,
    'jadro': 1,
    'slunce': 1,
    'vitr': 1,
    'biomasa': 1,
    'odpad': 1,
    'ostatni_oze': 1,
}


@pytest.mark.skip(reason="This is calling Entsoe API")
def test_get_production():
    params = entsoe.entsoe_params.copy()
    params["TimeInterval"] = '2022-02-25T11%2F2022-02-25T12'
    data = entsoe.request_data(entsoe.ENTSOE_URL, params)
    assert data
    production = entsoe.parse_xml(data, entsoe.ENTSOE_SOURCE_MAPPING)
    assert production['biomasa'] == 264
    assert production['uhli_cerne'] == 193
    assert production['uhli_hnede'] == 3876
    assert production['plyn'] == 582
    assert production['jadro'] == 3496


@pytest.mark.skip(reason="This is calling Entsoe API")
def test_get_data():
    # Get energy for past hour from Entsoe API
    data = entsoe.get_data()
    # These sources produce electricity all the time with more than zero share
    assert data['plyn'] > 0
    assert data['uhli'] > 0
    assert data['jadro'] > 0


def test_get_past_hour_param():
    past_hour_param = entsoe.get_past_hour_param()
    today_string = datetime.datetime.now().strftime(format='%Y-%m-%d')
    assert isinstance(past_hour_param, str)
    assert today_string in past_hour_param
    assert '%2F' in past_hour_param


def test_group_production():
    grouped_production = entsoe.group_production(sample_production)
    assert grouped_production == sample_grouped_production


def test_reorder_production():
    reordered_production = entsoe.reorder_production(sample_grouped_production)
    assert (
        list(reordered_production.keys())[0]
        == list(sample_reordered_production.keys())[0]
    )
    assert (
        list(reordered_production.keys())[1]
        == list(sample_reordered_production.keys())[1]
    )
