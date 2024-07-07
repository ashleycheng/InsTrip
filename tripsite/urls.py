from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAdminUser
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from trips.views import city, country, home
    
api_urlpatterns = [
    path('', include('trips.urls')),
]

auth_urlpatterns = [
    path('', obtain_jwt_token, name='get-token'),
    path('refresh/', refresh_jwt_token, name='refresh-token'),
    # path('verify/', verify_token, name='verify-token'),
    # path('permissions/', include(('app.permissions.urls', 'permissions'))),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path('docs/', include_docs_urls(
        title='InsTrip API',
        permission_classes=[IsAdminUser]
    )),
    path('api/', include((api_urlpatterns, 'api'))),
    path('auth/', include((auth_urlpatterns, 'api-auth'))),
    path("instrip/", home, name="home"),
    path("instrip/country/<str:country_name>/", country, name="country"),
    path("instrip/city/<str:city_name>/", city, name="city"),
]
