from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"noprizFizs", views.NoprizFizViewSet, basename="NoprizFizs")
urlpatterns = router.urls
