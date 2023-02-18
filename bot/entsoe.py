import datetime
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
import requests
import xmltodict  # type: ignore


load_dotenv()


ENTSOE_URL = 'https://web-api.tp.entsoe.eu/api?'

ENTSOE_SECURITY_TOKEN = os.getenv('ENTSOE_TOKEN')

# Complete parameter list in Entsoe API documentation.
# https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_psrtype
ENTSOE_SOURCE_MAPPING = {
    'B01': 'biomasa',
    'B02': 'uhli_hnede',
    'B03': 'uhli_plyn',
    'B04': 'plyn',
    'B05': 'uhli_cerne',
    'B06': 'ropa',
    'B11': 'voda',
    'B12': 'voda_rezervoar',
    'B14': 'jadro',
    'B15': 'ostatni_oze',
    'B16': 'slunce',
    'B17': 'odpad',
    'B19': 'vitr',
}

entsoe_params = {
    'securityToken': ENTSOE_SECURITY_TOKEN,
    'In_Domain': '10YCZ-CEPS-----N',
    'ProcessType': 'A16',
    'DocumentType': 'A75',
    'TimeInterval': None,
}


def request_data(url: str, params: Dict[str, Any]) -> Optional[str]:
    """Request data about energy production from Entsoe API.

    Args:
        url (str): Entsoe API url.
        params (Dict[str, str]): Parameters for the API get requests.

    Returns:
        Optional[str]: If response status is ok returns xml response as a string.
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0'
    }
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        return r.text
    return None


def parse_xml(xml: str, mapping: Dict[str, str]) -> Dict[str, int]:
    """Parse energy production from xml string for each resource type.

    Args:
        xml (str): XML response from Entsoe.
        mapping (Dict[str, str]): Mapping from Entsoe resource type codes to Czech names,
        e.g. from 'B01' to 'biomasa'.

    Returns:
        Dict[str, int]: Dictionary with production in MW for each resource type.
    """
    d = xmltodict.parse(xml)
    energy = {}

    for serie in d['GL_MarketDocument']['TimeSeries']:
        psr_type = serie['MktPSRType']['psrType']
        quantity = serie['Period']['Point']['quantity']
        if psr_type in mapping:
            energy[mapping[psr_type]] = int(quantity)

    return energy


def get_past_hour_param() -> str:
    """Get timeinterval for Entsoe API call representing past hour.

    Bot will run as a cron job, e.g. 05 7-18 * * *

    Returns:
        str: Timeinterval param for Entsoe API call, e.g. '2021-07-07T05%2F2021-07-07T06'
    """
    start = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat(
        timespec='hours'
    )
    end = datetime.datetime.utcnow().isoformat(timespec='hours')
    # %2F as backslash for the get request timeinterval parameter
    past_hour = start + '%2F' + end
    return past_hour


def group_production(production: Dict[str, int]) -> Dict[str, int]:
    """Group various types of coal (e.g. lignite, hard coal) and hydro (river, reservoir).

    Args:
        production (Dict[str, int]): Dictionary with production for each resource type.

    Returns:
        Dict[str, int]: Dictionary with production for each resource type.
        Only one entry for various types of coal.
    """
    grouped_prod: Dict[str, int] = {}

    for k, v in production.items():
        if k.startswith('uhli'):
            grouped_prod['uhli'] = grouped_prod.setdefault('uhli', 0) + v
        elif k.startswith('voda'):
            grouped_prod['voda'] = grouped_prod.setdefault('voda', 0) + v
        else:
            grouped_prod[k] = v

    return grouped_prod


def reorder_production(production: Dict[str, int]) -> Dict[str, int]:
    """Sort by production in descending order.

    Args:
        production (Dict[str, int]): Dictionary with production for each resource type.

    Returns:
        Dict[str, int]: Dictionary with production for each resource type.
    """
    return dict(sorted(production.items(), key=lambda items: items[1], reverse=True))


def get_data(
    timeinterval: str = None,
    url: str = ENTSOE_URL,
    params: Dict[str, Any] = entsoe_params,
    source_codes: Dict[str, str] = ENTSOE_SOURCE_MAPPING,
) -> Optional[Dict[str, int]]:
    """Get electricity production from Entsoe.

    Args:
        url (str, optional): Entsoe production API url. Defaults to ENTSOE_URL.
        params (Dict[str, str], optional): Params to call Entsoe API except TimeInterval.
        Defaults to entsoe_params.
        source_codes (Dict[str, str], optional): Mapping from Entsoe resource type codes to Czech labels.
        Defaults to ENTSOE_SOURCE_MAPPING.

    Returns:
        Optional[Dict[str, int]]: Dictionary with resource type as a key and energy production as value (descending order by value).
    """
    # Update params to request production for previous hour
    if not timeinterval:
        timeinterval = get_past_hour_param()
    params['TimeInterval'] = timeinterval

    # Get a xml string with data
    data = request_data(url, params)

    if data:
        production = parse_xml(data, source_codes)
        grouped_production = group_production(production)
        reordered_production = reorder_production(grouped_production)
        return reordered_production
    else:
        return None
