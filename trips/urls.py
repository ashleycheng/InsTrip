from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'top/city/(?P<country>.+?)', views.TopCityViewSet)
router.register(r'top/location/(?P<city>.+?)', views.TopLocationViewSet)
router.register(r'city/(?P<city>.+?)', views.CityInfoViewSet, 'city')
urlpatterns = [
    path('', include(router.urls)),
]
