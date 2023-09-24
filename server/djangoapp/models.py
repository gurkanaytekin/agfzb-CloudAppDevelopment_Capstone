from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# A plain Python class to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name  # Full name of dealership
        self.id = id  # Dealership id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st  # State alpha code
        self.state = state  # Full state name
        self.zip = zip
        self.idx = 0

    def __str__(self):
        return self.full_name + ", " + self.state


# <HINT> Create a plain Python class `DealerReview` to hold review data
