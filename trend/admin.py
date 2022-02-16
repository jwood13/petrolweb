from django.contrib import admin

# Register your models here.
from .models import Fuel_Price, Station


class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'postcode', 'state')


class Fuel_PriceAdmin(admin.ModelAdmin):
    list_display = ('station', 'fuel', 'price', 'time')
    list_filter = ['time']


admin.site.register(Station, StationAdmin)
admin.site.register(Fuel_Price, Fuel_PriceAdmin)
