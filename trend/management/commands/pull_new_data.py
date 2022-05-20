from django.core.management import BaseCommand
# Schedule Calling https://django.cowhite.com/blog/scheduling-taks-in-django/
# Heroku Scheduling https://medium.com/analytics-vidhya/schedule-a-python-script-on-heroku-a978b2f91ca8

# Import the model
from trend.api_calls import pull_prices


class Command(BaseCommand):
    # Show this when the user types help
    help = "Pulls new data from the Fuelcheck API"

    def handle(self, *args, **options):
        print("Pulling New Data")
        pull_prices()
