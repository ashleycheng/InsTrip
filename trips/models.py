from django.db import models

class IgPost(models.Model):
    # The composite primary key (shortcode, date, counrty) found, that is not supported. The first column is selected.
    shortcode = models.CharField(primary_key=True, max_length=30)
    owner_id = models.CharField(max_length=30)
    content = models.TextField(blank=True, null=True)
    date = models.DateField()
    location_id = models.CharField(max_length=30, blank=True, null=True)
    location_name = models.CharField(max_length=100, blank=True, null=True)
    location_city = models.CharField(max_length=50, blank=True, null=True)
    counrty = models.CharField(max_length=30)
    has_location = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'IgPost'
        unique_together = (('shortcode', 'date', 'counrty'),)


class IgLocation(models.Model):
    location_id = models.CharField(primary_key=True, max_length=30)
    location_name = models.CharField(max_length=100)
    location_city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    lat = models.CharField(max_length=30, blank=True, null=True)
    lng = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'IgLocation'

    @classmethod
    def get_address(cls):
        query = cls.objects.all().values_list('location_name', 'address')
        return {q[0]: q[1] for q in query}
    

class CityInfo(models.Model):
    # city = models.CharField(max_length=80)
    city_name = models.CharField(max_length=30)
    city_name_ch = models.CharField(max_length=30)
    image = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'CityInfo'


class LocationMap(models.Model):
    location_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'LocationMap'

    @classmethod
    def get_location_map(cls):
        query = cls.objects.all()
        return {q.location_name: q.location for q in query}


class CountryInfo(models.Model):
    country_name = models.CharField(max_length=30)
    country_name_ch = models.CharField(max_length=30)
    image = models.URLField(blank=True, null=True)
    analysis = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'CountryInfo'
