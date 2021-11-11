import requests
import os
import uuid
import json
import time
import datetime

from .models import Fuel_Price, Station


def get_access_token():
    '''
    Get the api access token from the security call

    Returns
    ----------
    access_token: Api Access Token string
    '''
    url = "https://api.onegov.nsw.gov.au/oauth/client_credential/accesstoken"

    querystring = {"grant_type": "client_credentials"}

    secret = os.environ['api_secret_b64']
    headers = {
        'content-type': "application/json",
        'authorization': secret
        }

    auth_response = requests.request("GET", url, headers=headers, params=querystring)
    access_token = auth_response.json()['access_token']
    return access_token


try:
    access_token = get_access_token()
except KeyError:
    access_token = ''


def get_local_prices(postcode, fueltype):
    '''
    Get prices of nearby stations based on a postcode and a fueltype

    Return
    -------------
    station data: {'stations': [{'brand', 'code', 'name', 'location':{'distance','latitude','longitude'}, 'state'}],
                   'prices': [{'stationcode', 'fueltype', 'lastupdated', 'state'}]
                   }
    '''
    url = "https://api.onegov.nsw.gov.au/FuelPriceCheck/v2/fuel/prices/location"
    transaction_id = uuid.uuid4()
    ts = time.gmtime()
    timestamp = time.strftime("%d/%m/%Y %I:%m:%S %p", ts)
    payload = {
        "fueltype": fueltype,
        "brand": [],
        "namedlocation": postcode,
        "referencepoint": {
            "latitude": "-34.045601",
            "longitude": "151.051056"
        },
        "sortby": "Price",
        "sortascending": "true"
    }
    payload_text = json.dumps(payload)
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': 'Bearer ' + access_token,
        'apikey': os.environ['api_key'],
        'transactionid': str(transaction_id),
        'requesttimestamp': timestamp
        }

    response = requests.request("POST", url, data=payload_text, headers=headers)
    station_data = response.json()
    if not response.ok:
        raise Exception(station_data)
    return station_data


def get_all_prices(full=False):
    '''
    Get prices of nearby stations based on a postcode and a fueltype

    Return
    -------------
    station data: {'stations': [{'brand', 'code', 'name', 'location':{'distance','latitude','longitude'}, 'state'}],
                   'prices': [{'stationcode', 'fueltype', 'lastupdated', 'state'}]
                   }
    '''
    if full:
        url = "https://api.onegov.nsw.gov.au/FuelPriceCheck/v2/fuel/prices/"
    else:
        url = "https://api.onegov.nsw.gov.au/FuelPriceCheck/v2/fuel/prices/new"
    transaction_id = uuid.uuid4()
    ts = time.gmtime()
    timestamp = time.strftime("%d/%m/%Y %I:%m:%S %p", ts)

    headers = {
        'authorization': 'Bearer ' + access_token,
        'content-type': 'application/json; charset=utf-8',
        'apikey': os.environ['api_key'],
        'transactionid': str(transaction_id),
        'requesttimestamp': timestamp,
        'states': 'NSW'
        }

    response = requests.request("GET", url, headers=headers)
    station_data = response.json()
    if not response.ok:
        raise Exception(station_data)
    return station_data


def pull_ref_data():
    '''
    Get the reference data from the nsw api

    Return
    ----------
    ref_data_response: {'brands': {'items': {'name', 'state}},
                        'fueltypes': {'items': {'code', 'name', 'state}},
                        'stations': {'items': {'brand', 'code', 'name', 'address', 'location':{'latitude', longitude'}, 'state'}},
                        'trend_periods': {'items': {}},
                        'sortfields': {'items': {}},
                        }
    '''
    url = "https://api.onegov.nsw.gov.au/FuelCheckRefData/v2/fuel/lovs"
    transaction_id = uuid.uuid4()
    ts = time.gmtime()
    timestamp = time.strftime("%d/%m/%Y %I:%M:%S %p", ts)

    querystring = {"states": "NSW"}

    headers = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': 'Bearer ' + access_token,
        'apikey': os.environ['api_key'],
        'transactionid': str(transaction_id),
        'requesttimestamp': timestamp,
        'if-modified-since': "01/01/2010 01:00:00 AM"
    }

    ref_data_response = requests.request(
        "GET", url, headers=headers, data=querystring)
    if not ref_data_response.ok:
        raise Exception(ref_data_response.json())
    # Save data so it doesn't need to be called again
    return ref_data_response.json()


def save_station_data(station_data):
    for s in station_data:
        station = Station(name=s['name'], brand=s['brand'], id=s['code'], address=s['address'], latitude=s['location']['latitude'], longitude=s['location']['longitude'], state=s['state'])
        station.save()


def pull_prices(full=False):
    price_data = get_local_prices('2232', 'E10')
    save_prices(price_data['prices'])


def save_prices(price_data):
    for p in price_data:
        # station = Station.objects.get(id=p['stationcode'])
        updated = datetime.datetime.strptime(p['lastupdated'], "%d/%m/%Y %H:%M:%S")
        price = Fuel_Price(station_id=p['stationcode'], fuel=p['fueltype'], time=updated, price=p['price'])
        price.save()
