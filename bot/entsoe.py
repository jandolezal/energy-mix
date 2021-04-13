import os
import datetime
import xml.etree.ElementTree as ET

import requests
from dotenv import load_dotenv

load_dotenv()


def request_data(url, params):
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0'
    }
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        return r.text
    return None


def parse_xml(xml, mapping):
    """Parse renewable energy from xml string.
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


def get_past_hour_param():
    # Get energy from past hour. Script will be a cronjob 15 7-18 * * *
    start = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat(timespec='hours')
    end = datetime.datetime.utcnow().isoformat(timespec='hours')
    # %2F as backslash for the get request timeinterval parameter
    past_hour = start + '%2F' + end
    return past_hour


def group_production(production):
    """Group coal production.
    """
    grouped_prod = {}

    for k, v in production.items():
        if k.startswith('uhli'):
            grouped_prod['uhli'] = grouped_prod.setdefault('uhli', 0) + v
        else:
            grouped_prod[k] = v

    return grouped_prod

def reorder_production(production):
    order = [
        'uhli', 'plyn', 'ropa', 'jadro', 'slunce', 'vitr',
        'voda', 'biomasa', 'odpad', 'ostatni_oze'
        ]
    
    ordered_production = {k: production[k] for k in order}

    return ordered_production


ENTSOE_URL = 'https://transparency.entsoe.eu/api?'

ENTSOE_SECURITY_TOKEN = os.getenv('ENTSOE_TOKEN')

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
    'TimeInterval': get_past_hour_param(),
    }
