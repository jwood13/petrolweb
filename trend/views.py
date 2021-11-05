from django.shortcuts import render
# from django.http import HttpResponse
# from requests import api
from . import api_calls
from .models import Fuel_Price, Station


# Create your views here.
def index(request):
    api_calls.pull_prices()
    station_data = api_calls.get_local_prices('2232', 'E10')
    current_lowest_price = station_data['prices'][0]['price']
    station_code = station_data['prices'][0]['stationcode']
    station_dict = {x['code']: x for x in station_data['stations']}
    return render(request, 'current.html', {'text': f"The lowest price for E10 is {current_lowest_price} at {station_dict[station_code]['name']}"})


def get_all_data(request):
    api_calls.pull_prices()
    station_code = '1112'
    fuel_code = 'E10'
    petrol_prices = Fuel_Price.objects.filter(station=station_code, fuel=fuel_code)
    petrol_price = petrol_prices[len(petrol_prices)-1].price
    station_name = Station.objects.get(id=station_code).name
    fuel_name = petrol_prices[len(petrol_prices)-1].fuel
    return render(request, 'current.html', {'text': f"The petrol price at {station_name} is ${petrol_price} for {fuel_name}"})


def register_stations(request):
    try:
        ref_data = api_calls.pull_ref_data()
        stations = ref_data['stations']['items']
        api_calls.save_station_data(stations)
        return_text = 'Success, Data loaded'
    except Exception as message:
        return_text = f'Failed to load data: {message}'
    return render(request, 'current.html', {'text': return_text})
