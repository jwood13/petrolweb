import requests
import os
from django.shortcuts import render
from django.http import HttpResponse
from requests import api
from . import api_calls

# Create your views here.
def index(request):
    station_data = api_calls.get_local_prices('2232','E10')
    current_lowest_price = station_data['prices'][0]['price']
    return HttpResponse(f"The lowest price for E10 is {current_lowest_price}")