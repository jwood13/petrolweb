from django.core.management import BaseCommand

# Import the model
from trend.models import Fuel_Price


class Command(BaseCommand):
    # Show this when the user types help
    help = "deletes all data from before 2022"

    def handle(self, *args, **options):
        print("Deleting old data")

        old_data = Fuel_Price.objects.filter(time__year__lte=2021)
        old_data.delete()
