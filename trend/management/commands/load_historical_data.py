from csv import DictReader
from django.core.management import BaseCommand

# Import the model
from trend.models import Fuel_Price


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from 2210.csv"

    def handle(self, *args, **options):

        # Show this before loading the data into the database
        print("Loading Historical Fuel data")

        # Code to load the data into database
        for row in DictReader(open('./2210_data.csv')):
            entry = Fuel_Price(
                station_id=row['StationCode'], time=row['PriceUpdatedDate'], fuel=row['FuelCode'], price=row['Price'])
            possible_duplicates = Fuel_Price.objects.filter(
                station_id=row['StationCode'], time=row['PriceUpdatedDate'], fuel=row['FuelCode'])
            if len(possible_duplicates) == 0:
                entry.save()
            else:
                print("Some data already present. Stopping")
                break
