from django.db import models

STATE_CHOICES = [('NSW', 'New South Wales'),
                 ('TAS', 'Tasmania')]

FUEL_CHOICES = [('E10', 'Ethanol 94'),
                ('U91', 'Unleaded 91'),
                ('E85', 'Ethanol 105'),
                ('P95', 'Premium 95'),
                ('P98', 'Premium 98'),
                ('DL', 'Diesel'),
                ('PDL', 'Premium Diesel'),
                ('B20', 'Biodiesel 20'),
                ('LPG', 'LPG'),
                ('CNG', 'CNG/NGV'),
                ('EV', 'EV charge'), ]

BRANDS_CHOICES = [('7-Eleven', '7-Eleven'),
                  ('Ampol', 'Ampol'),
                  ('BP', 'BP'),
                  ('Budget', 'Budget'),
                  ('Caltex', 'Caltex'),
                  ('Caltex Woolworths', 'Caltex Woolworths'),
                  ('Coles Express', 'Coles Express'),
                  ('Costco', 'Costco'),
                  ('Enhance', 'Enhance'),
                  ('Independent', 'Independent'),
                  ('Inland Petroleum', 'Inland Petroleum'),
                  ('Liberty', 'Liberty'),
                  ('Lowes', 'Lowes'),
                  ('Matilda', 'Matilda'),
                  ('Metro Fuel', 'Metro Fuel'),
                  ('Mobil', 'Mobil'),
                  ('Mobil 1', 'Mobil 1'),
                  ('NRMA', 'NRMA'),
                  ('Prime Petroleum', 'Prime Petroleum'),
                  ('Puma Energy', 'Puma Energy'),
                  ('Shell', 'Shell'),
                  ('South West', 'South West'),
                  ('Speedway', 'Speedway'),
                  ('Tesla', 'Tesla'),
                  ('Transwest Fuels', 'Transwest Fuels'),
                  ('United', 'United'),
                  ('Westside', 'Westside'),
                  ('Woodham Petroleum', 'Woodham Petroleum'), ]


# Create your models here.
class Station(models.Model):
    station_name = models.CharField(max_length=10)
    brand = models.CharField(max_length=30, choices=BRANDS_CHOICES)
    address = models.CharField(max_length=200)
    postcode = models.SmallIntegerField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    state = models.CharField(max_length=3, choices=STATE_CHOICES)

    def __str__(self):
        return self.station_name


class Fuel_Price(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    time = models.DateTimeField('Update time')
    fuel = models.CharField("Fuel Type", max_length=3, choices=FUEL_CHOICES)
    price = models.FloatField()

    def __str__(self):
        return f"{self.station}-{self.fuel}: ${self.price:%2f}"
