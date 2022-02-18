from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update_prices', views.get_all_data, name='get_data'),
    path('register_stations', views.register_stations, name='register_stations'),
    path('<int:station_id>', views.station_history, name='current_station'),
    path('history/<int:station_id>', views.station_history, name='station_history')


]
