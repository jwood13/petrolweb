from django.shortcuts import render
from django.http import Http404
# from django.http import HttpResponse
# from requests import api
from . import api_calls
from .models import Fuel_Price, Station
from plotly.offline import plot
import plotly.graph_objs as go
import bokeh
from bokeh import plotting


# Create your views here.
def index(request):
    '''
    Default Home Page
    Pulls in local prices for a given postcode saves them and then displays them
    '''
    api_calls.pull_prices()
    station_data = api_calls.get_local_prices('2210', 'E10')
    station_dict = {x['code']: x for x in station_data['stations']}
    prices = [{'price': x['price'], 'station':station_dict[x['stationcode']]
               ['name'], 'fuel':x['fueltype'], 'station_code': x['stationcode']} for x in station_data['prices']]
    print(prices)
    return render(request, 'current.html', {'Header': 'Current Prices:', 'petrol_prices': prices})


def get_all_data(request):
    api_calls.pull_prices()
    # TODO get most recent value for each station, rather than filtering each individually
    station_code = '18163'
    fuel_code = 'E10'
    petrol_prices = Fuel_Price.objects.filter(
        station=station_code, fuel=fuel_code)
    if not petrol_prices:
        raise Http404(f"No E10 price data for station {station_code}")
    return render(request, 'current.html', {'Header': 'Current Prices:', 'petrol_prices': petrol_prices})


def register_stations(request):
    '''
    /register_stations
    Update the stations list from the api
    '''
    try:
        ref_data = api_calls.pull_ref_data()
        stations = ref_data['stations']['items']
        api_calls.save_station_data(stations)
        return_text = 'Success, Data loaded'
    except Exception as message:
        return_text = f'Failed to load data: {message}'
    return render(request, 'current.html', {'text': return_text})


def station_history(request, station_id):
    '''
    /history/station_id
    show historical data for a given station
    '''
    try:
        station_name = Station.objects.get(id=station_id).name
    except Station.DoesNotExist:
        raise Http404(f"No station with id {station_id}")
    price_history = Fuel_Price.objects.filter(
        station=station_id, fuel='E10').order_by('time')
    if not price_history:
        raise Http404(f"No E10 price data for station {station_name}")

    # Make a Plot
    fig = go.Figure()
    prices = [x.price/100 for x in price_history]
    dates = [x.time for x in price_history]
    scatter = go.Scatter(x=dates, y=prices,
                         name='test',
                         opacity=0.8, marker_color='green')
    fig.add_trace(scatter)
    plt_div = plot(fig, output_type='div')

    p = plotting.figure(plot_width=480, plot_height=300,
                        x_axis_type='datetime', title=f'Price history for {station_name}')

    p.line(dates, prices)
    p.scatter(dates, prices)

    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.yaxis.formatter = bokeh.models.NumeralTickFormatter(format='$0.00')

    bscript, bdiv = bokeh.embed.components(p)

    return render(request, 'graph.html', {'plot_div': plt_div, 'plot_script': bscript, 'bokeh_div': bdiv, 'text': f'This is the history for {station_name}'})
