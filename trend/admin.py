from django.contrib import admin

# Register your models here.
from .models import Fuel_Price, Station

admin.site.register(Station)
admin.site.register(Fuel_Price)