import requests
import os
import uuid
import json
import time

def get_access_token():
    '''
    Get the api access token from the security call

    Returns
    ----------
    access_token: Api Access Token string
    '''
    url = "https://api.onegov.nsw.gov.au/oauth/client_credential/accesstoken"

    querystring = {"grant_type":"client_credentials"}

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

def get_local_prices(postcode,fueltype):
    '''
    Get prices of nearby stations based on a postcode and a fueltype

    Return
    -------------
    station data: dict of relevant data
                'stations'contains station data
                'prices' contains relevant price data
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
    payload_text=json.dumps(payload)
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': 'Bearer '+access_token,
        'apikey': os.environ['api_key'],
        'transactionid': str(transaction_id),
        'requesttimestamp': timestamp
        }

    response = requests.request("POST", url, data=payload_text, headers=headers)
    station_data = response.json()
    return station_data

