from django_filters import rest_framework as rest_framework_filters
from nopriz.models import *


class NoprizFizFilter(rest_framework_filters.FilterSet):
    is_valid = rest_framework_filters.BooleanFilter()
    verified_id_number = rest_framework_filters.BooleanFilter()
    verified_full_name = rest_framework_filters.BooleanFilter()

    class Meta:
        model = NoprizFiz
        fields = ["is_valid", "verified_id_number", "verified_full_name"]
