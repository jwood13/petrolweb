import os
from django.shortcuts import render
from django.http import Http404
# from django.http import HttpResponse
# from requests import api
from . import api_calls
from .models import Fuel_Price, Station
import bokeh
from bokeh import plotting
from bokeh.models import GMapOptions, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.plotting import gmap
from bokeh.transform import transform


# Create your views here.
def index(request):
    '''
    Default Home Page
    Pulls in local prices for a given postcode saves them and then displays them
    '''
    api_calls.pull_prices()
    station_data = api_calls.get_local_prices('2210', 'E10')
    station_dict = {x['code']: x for x in station_data['stations']}
    prices = [{'price': x['price'], 'station':station_dict[x['stationcode']],
               'fuel':x['fueltype'], 'station_code': x['stationcode']} for x in station_data['prices']]
    print(prices)

    latitudes = [x['station']['location']['latitude'] for x in prices]
    longitudes = [x['station']['location']['longitude'] for x in prices]
    centre_latitude = sum(latitudes)/len(latitudes)
    centre_longitude = sum(longitudes)/len(longitudes)
    names = [x['station']['name'] for x in prices]
    station_price = [x['price']/100 for x in prices]
    station_codes = [x['station_code'] for x in prices]
    data = dict(lat=latitudes,
                lon=longitudes, name=names, price=station_price, code=station_codes)
    map_options = GMapOptions(lat=centre_latitude, lng=centre_longitude, map_type="roadmap", zoom=13)
    # Replace the value below with your personal API key:
    api_key = os.environ["google_maps_api_key"]

    p = gmap(api_key, map_options, plot_width=640, plot_height=400, toolbar_location=None)

    color_mapper = LinearColorMapper(palette="Plasma256", low=min(station_price), high=max(station_price))
    color_bar = ColorBar(color_mapper=color_mapper, title='Price', formatter=NumeralTickFormatter(format="$0.00"))
    p.add_layout(color_bar, 'right')

    p.add_tools(bokeh.models.HoverTool(tooltips=[("Name", '@name'), ("Price", '@price{$0.00}')]))
    p.circle(x="lon", y="lat", size=15, fill_color=transform('price', color_mapper), fill_alpha=0.8, line_width=0.0, source=data)

    p.xaxis.visible = False
    p.yaxis.visible = False

    bscript, bdiv = bokeh.embed.components(p)
    return render(request, 'current.html', {'Header': 'Current Prices:', 'petrol_prices': prices,
                                            'plot_script': bscript, 'bokeh_div': bdiv})


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
    prices = [x.price/100 for x in price_history]
    dates = [x.time for x in price_history]
    data = {'date': dates, 'price': prices}

    p = plotting.figure(plot_width=640, plot_height=400,
                        x_axis_type='datetime', title=f'Price history for {station_name}', toolbar_location=None)
    p.line('date', 'price', source=data,)
    p.scatter('date', 'price', source=data, hover_line_color='green')

    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.yaxis.formatter = bokeh.models.NumeralTickFormatter(format='$0.00')
    p.add_tools(bokeh.models.HoverTool(tooltips=[("Price", '@price{$0.00}'), ("Date", '@date{%d/%m}')], formatters={'@date': 'datetime'}))
    bscript, bdiv = bokeh.embed.components(p)

    return render(request, 'graph.html', {'plot_script': bscript, 'bokeh_div': bdiv, 'text': f'This is the history for {station_name}'})
