import datetime
import os
from typing import Dict, Optional
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import requests


load_dotenv()


ENTSOE_URL = 'https://transparency.entsoe.eu/api?'

ENTSOE_SECURITY_TOKEN = os.getenv('ENTSOE_TOKEN')

# Complete parameter list in Entsoe API documentation.
# https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_psrtype
ENTSOE_SOURCE_MAPPING = {
    'B01': 'biomasa',
    'B02': 'uhli_hnede',
    'B03': 'uhli_plyn',
    'B04': 'plyn',
    'B05': 'uhli_cerne',
    'B06': 'ropa',
    'B11': 'voda',
    'B14': 'jadro',
    'B15': 'ostatni_oze',
    'B16': 'slunce',
    'B17': 'odpad',
    'B19': 'vitr',
    }

ENTSOE_PARAMS = {
    'securityToken': ENTSOE_SECURITY_TOKEN,
    'In_Domain': '10YCZ-CEPS-----N',
    'ProcessType': 'A16',
    'DocumentType': 'A75',
    'TimeInterval': None,
    }


def request_data(url: str, params: Dict[str, str]) -> Optional[str]:
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


def parse_xml(xml:str, mapping: Dict[str, str]) -> Dict[str, int]:
    """Parse energy production from xml string for each resource type.

    Args:
        xml (str): XML response from Entsoe.
        mapping (Dict[str, str]): Mapping from Entsoe resource type codes to Czech names,
        e.g. from 'B01' to 'biomasa'.

    Returns:
        Dict[str, int]: Dictionary with production in MW for each resource type.
    """
    energy = {}
    root = ET.fromstring(xml)
    ns = '{urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0}'
    for serie in root.iter(ns + 'TimeSeries'):
        psr_type = serie.find(ns + 'MktPSRType').find(ns + 'psrType').text
        quantity = serie.find(ns + 'Period').find(ns + 'Point').find(ns + 'quantity').text
        if psr_type in mapping:
            energy[mapping[psr_type]] = int(quantity)
    return energy


def get_past_hour_param() -> str:
    """Get timeinterval for Entsoe API call representing past hour.

    Bot will run as a cron job, e.g. 05 7-18 * * *

    Returns:
        str: Timeinterval param for Entsoe API call, e.g. '2021-07-07T05%2F2021-07-07T06'
    """
    start = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat(timespec='hours')
    end = datetime.datetime.utcnow().isoformat(timespec='hours')
    # %2F as backslash for the get request timeinterval parameter
    past_hour = start + '%2F' + end
    return past_hour


def get_udated_params(params: Dict[str, str]) -> Dict[str, str]:
    timeinterval = get_past_hour_param()
    params['TimeInterval'] = timeinterval

    return params


def group_production(production: Dict[str, int]) -> Dict[str, int]:
    """Group various types of coal (e.g. lignite, hard coal).

    Args:
        production (Dict[str, int]): Dictionary with production for each resource type.

    Returns:
        Dict[str, int]: Dictionary with production for each resource type.
        Only one entry for various types of coal.
    """
    grouped_prod = {}

    for k, v in production.items():
        if k.startswith('uhli'):
            grouped_prod['uhli'] = grouped_prod.setdefault('uhli', 0) + v
        else:
            grouped_prod[k] = v

    return grouped_prod


def reorder_production(production: Dict[str, int]) -> Dict[str, int]:
    """Reorder production.

    Args:
        production (Dict[str, int]): Dictionary with production for each resource type.

    Returns:
        Dict[str, int]: Dictionary with production for each resource type.
    """
    order = [
        'uhli', 'plyn', 'ropa', 'jadro', 'slunce', 'vitr',
        'voda', 'biomasa', 'odpad', 'ostatni_oze'
        ]
    
    ordered_production = {k: production[k] for k in order}

    return ordered_production
 

def get_data(
    url: str =ENTSOE_URL,
    default_params: Dict[str, str] = ENTSOE_PARAMS,
    mapping: Dict[str, str] = ENTSOE_SOURCE_MAPPING
    ) -> Optional[Dict[str, int]]:
    """Get electricity production from Entsoe.

    Args:
        url (str, optional): Entsoe production API url. Defaults to ENTSOE_URL.
        default_params (Dict[str, str], optional): Placeholder params for get request. 
        Defaults to ENTSOE_PARAMS.
        mapping (Dict[str, str], optional): Mapping from Entsoe resource type codes to Czech labels. 
        Defaults to ENTSOE_SOURCE_MAPPING.

    Returns:
        Optional[Dict[str, int]]: [description]
    """

    params = get_udated_params(default_params)
    data = request_data(url, params)

    if data:
        production = parse_xml(data, mapping)
        grouped_production = group_production(production)
        reordered_production = reorder_production(grouped_production)
        return reordered_production
    else:
        return None
