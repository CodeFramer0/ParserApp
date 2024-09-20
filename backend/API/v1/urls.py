from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Parser API",
        default_version="v1",
        description="API documentation for Parser application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"noprizFizs", views.NoprizFizViewSet, basename="NoprizFizs")
router.register(r"noprizYrs", views.NoprizYrViewSet, basename="NoprizYrs")

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", include(router.urls)),
]
