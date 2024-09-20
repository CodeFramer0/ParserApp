from rest_framework import serializers

from nopriz.models import *


class NoprizFizSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoprizFiz
        fields = "__all__"
        read_only_fields = (
            "id",
            "id_number_img",
            "full_name_img",
            "date_of_inclusion_protocol_img",
            "date_of_modification_img",
        )


class NoprizYrSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoprizYr
        fields = "__all__"
