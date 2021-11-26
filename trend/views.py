from django.shortcuts import render
# from django.http import HttpResponse
# from requests import api
from . import api_calls
from .models import Fuel_Price, Station
from plotly.offline import plot
import plotly.graph_objs as go


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
    petrol_prices = Fuel_Price.objects.filter(
        station=station_code, fuel=fuel_code)
    if len(petrol_prices) > 0:
        petrol_price = petrol_prices[len(petrol_prices)-1].price
        fuel_name = petrol_prices[len(petrol_prices)-1].fuel
    else:
        petrol_price = 0
        fuel_name = 'N/A'
    station_name = Station.objects.get(id=station_code).name
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


def station_history(request, station_id):
    price_history = Fuel_Price.objects.filter(station=station_id, fuel='E10')
    station_name = Station.objects.get(id=station_id).name

    fig = go.Figure()
    prices = [x.price for x in price_history]
    dates = [x.time for x in price_history]
    scatter = go.Scatter(x=dates, y=prices,
                         name='test',
                         opacity=0.8, marker_color='green')
    fig.add_trace(scatter)
    plt_div = plot(fig, output_type='div')
    return render(request, 'graph.html', {'plot_div': plt_div, 'text': f'This is the history for station {station_name}'})
