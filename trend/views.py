from django.shortcuts import render
# from django.http import HttpResponse
# from requests import api
from . import api_calls


# Create your views here.
def index(request):
    station_data = api_calls.get_local_prices('2232', 'E10')
    current_lowest_price = station_data['prices'][0]['price']
    station_code = station_data['prices'][0]['stationcode']
    station_dict = {x['code']: x for x in station_data['stations']}
    return render(request, 'current.html', {'text': f"The lowest price for E10 is {current_lowest_price} at {station_dict[station_code]['name']}"})


def register_stations(request):
    try:
        ref_data = api_calls.pull_ref_data()
        stations = ref_data['stations']['items']
        api_calls.save_station_data(stations)
        return_text = 'Success, Data loaded'
    except DatabaseError:
        return_text = 'Failed to load data'
    return render(request, 'current.html', {'text': return_text})
