from rest_framework import serializers
from .models import IgPost, IgLocation, CityInfo


class CityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityInfo
        fields = '__all__'


class IgLocationSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField('get_ig_post')

    def get_ig_post(self, obj):
        post = IgPost.objects.filter(location_id=obj.location_id).values_list('shortcode', 'owner_id')
        owners = set()
        post_list = []
        for i in post:
            if i[1] not in owners:
                post_list.append(i[0])
            owners.add(i[1])
        return post_list[:4]
    
    class Meta:
        model = IgLocation
        fields = ('location_name', 'address', 'posts')

