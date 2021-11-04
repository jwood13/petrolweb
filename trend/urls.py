from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register_stations', views.register_stations, name='register_stations')
]
