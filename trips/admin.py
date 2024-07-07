from django.contrib import admin
from django.utils.html import format_html
from .models import CityInfo, LocationMap, CountryInfo

# Register your models here.

class CityInfoAdmin(admin.ModelAdmin):
    def display_image(self, obj):
        return format_html('<img src="{}" width="200"/>'.format(obj.image))
    
    list_display = ('city_name', 'city_name_ch', 'display_image')
    readonly_fields = ('display_image',)
    ordering = ("id",)

class LocationMapAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location')

class CountryInfoMapAdmin(admin.ModelAdmin):
    list_display = ('country_name',)

admin.site.register(CityInfo, CityInfoAdmin)
admin.site.register(LocationMap, LocationMapAdmin)
admin.site.register(CountryInfo, CountryInfoMapAdmin)
