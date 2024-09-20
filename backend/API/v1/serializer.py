from nopriz.models import *
from rest_framework import serializers


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
