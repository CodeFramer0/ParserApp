from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from nopriz.models import *
from nostroy.models import *
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .filters import *
from .serializer import *


class NoprizFizViewSet(viewsets.ModelViewSet):
    serializer_class = NoprizFizSerializer
    queryset = NoprizFiz.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    filterset_class = NoprizFizFilter


class NoprizYrViewSet(viewsets.ModelViewSet):
    serializer_class = NoprizYrSerializer
    queryset = NoprizYr.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    filterset_class = NoprizYrFilter


# class NostroySmetViewSet(viewsets.ModelViewSet):
#     serializer_class = NoprizFizSerializer
#     queryset = NostroySmet.objects.all().order_by("id")
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     filterset_class = NostroySmetFilter
