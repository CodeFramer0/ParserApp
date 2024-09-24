from django_filters import rest_framework as rest_framework_filters
from nopriz.models import *
from nostroy.models import *


class NoprizFizFilter(rest_framework_filters.FilterSet):
    is_parsed = rest_framework_filters.BooleanFilter()
    verified_id_number = rest_framework_filters.BooleanFilter()

    class Meta:
        model = NoprizFiz
        fields = [
            "is_parsed",
            "verified_id_number",
        ]


class NoprizYrFilter(rest_framework_filters.FilterSet):
    class Meta:
        model = NoprizYr
        fields = [
            "id_number",
        ]
