import django_filters
from . models import Bike
import floppyforms

class BikeFilter(django_filters.FilterSet):
    class Meta:
        model=Bike
        fields = ['bike_name']
