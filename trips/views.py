from collections import Counter

import requests
from django.db.models import Q
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import CityInfo, IgLocation, IgPost, LocationMap, CountryInfo
from .serializers import CityInfoSerializer, IgLocationSerializer


def home(request):
    return render(request, 'home.html', {})


def get_photo(keyword):
    r = requests.get(f'https://api.pexels.com/v1/search?query={keyword}&per_page=5', headers={
                     'Authorization': 'AKI1XnhKI4dAix0UkqJeptXKQORB9XZveHy8UmsinQkIL1nHV9yhzG5J'})
    res = r.json()
    for i in res['photos']:
        if i['width'] > i['height']:
            return i['src']['medium']


def country(request, country_name):
    country_trans = {
        "japan": "日本",
        "korea": "韓國",
        "vietnam": "越南",
        "thai": "泰國",
    }
    queryset = IgPost.objects.filter(counrty=country_trans[country_name], has_location=1).exclude(
        location_city__contains='Taiwan').exclude(location_city__contains='Taoyuan').values_list('location_city', flat=True)
    if country_name == 'Japan':
        city = [i.replace(', Japan', '').replace('Shinjuku', 'Shinjuku, Tokyo').split(
            ',')[-1].strip() for i in queryset if i != '']
    elif country_name == 'korea':
        city = [i.replace(', Korea', '').replace(', South Korea', '').split(
            ',')[-1].strip() for i in queryset if i != '']
    elif country_name == 'vietnam':
        city = [i.replace(f', {country_name.title()}', '').replace('Ðà Nẵng', 'Da Nang').replace(
            'Quang Nam-Da Nang', 'Da Nang').split(',')[-1].strip() for i in queryset if i != '']
    else:
        city = [i.replace(f', {country_name.title()}', '').split(
            ',')[-1].strip() for i in queryset if i != '']
    counter = Counter(city)
    top_city = [i[0] for i in counter.most_common(5)]
    res = []
    for city in top_city:
        info = CityInfo.objects.get(city_name=city)
        res.append((city, info.city_name_ch,
                   info.image, info.description[:60]))
    return render(request, 'country.html', {'country_name': country_name, 'country_name_ch': country_trans[country_name], 'top_city': res})


def get_top_location(location_ids):
    query = IgPost.objects.filter(location_id__in=location_ids)
    q = query.values_list('location_name', 'owner_id')
    # 計算地標打卡數量，不重複計算同一個帳號的貼文
    owners = set()
    loc_list = []
    for location_name, owner_id in q:
        if owner_id not in owners:
            loc_list.append(location_name)
            owners.add(owner_id)

    loc_map = LocationMap.get_location_map()
    # 同一個地標如果存在不同的打卡標籤，會用相同的名稱做替換
    location = [loc_map[i] if i in loc_map.keys() else i for i in loc_list]
    counter = Counter(location)
    top_loc = [i[0] for i in counter.most_common(5) if i[1]]
    address = IgLocation.get_address()
    res = []
    for loc in top_loc:
        post = query.filter(location_name=loc).values_list(
            'shortcode', 'owner_id')
        owners = set()
        post_list = []
        for i in post:
            if i[1] not in owners:
                post_list.append(i[0])
            owners.add(i[1])
        try:
            add = address[loc]
        except:
            add = None
        res.append(
            {'location_name': loc, 'address': add, 'post': post_list[:4]})
    return res


def city(request, city_name):
    city_info = CityInfo.objects.get(city_name__iexact=city_name)
    query = IgLocation.objects.filter(location_city__icontains=city_name)
    tag_spot = query.filter(Q(category='地標和名勝古蹟') | Q(category__in=[
                            '公園', '國家公園', '河流', '旅遊與交通運輸', '海灘', '橋樑', '島嶼', '峽灣'])).values_list('location_id', flat=True)
    tag_restaurant = query.filter(Q(category__icontains='餐廳') | Q(category__icontains='麵店') | Q(
        category__icontains='燒烤店') | Q(category__in=['壽司店', '三明治店'])).values_list('location_id', flat=True)
    tag_coffee = query.filter(Q(category__icontains='咖啡') | Q(category__icontains='甜點') | Q(
        category__icontains='烘焙') | Q(category__in=['茶店', ])).values_list('location_id', flat=True)
    tag_shopping = query.filter(Q(category__icontains='購物') | Q(category__icontains='市場') | Q(
        category__icontains='商家') | Q(category__in=['雜貨店', ])).values_list('location_id', flat=True)
    tag_fun = query.filter(Q(category__in=['藝術與娛樂', '動物園', '水族館', '博物館', '遊樂主題公園']) | Q(
        category__icontains='美術館')).values_list('location_id', flat=True)

    tag_spot_res = get_top_location(tag_spot)
    tag_restaurant_res = get_top_location(tag_restaurant)
    tag_coffee_res = get_top_location(tag_coffee)
    tag_shopping_res = get_top_location(tag_shopping)
    tag_fun_res = get_top_location(tag_fun)

    result = []
    if tag_spot_res:
        result.append({'tag': '觀光景點', 'location': tag_spot_res})
    if tag_restaurant_res:
        result.append({'tag': '餐廳', 'location': tag_restaurant_res})
    if tag_coffee_res:
        result.append({'tag': '咖啡廳', 'location': tag_coffee_res})
    if tag_shopping_res:
        result.append({'tag': '逛街', 'location': tag_shopping_res})
    if tag_fun_res:
        result.append({'tag': '休閒', 'location': tag_fun_res})

    return render(request, 'city.html',
                  {'city_name': city_name, 'city_name_ch': city_info.city_name_ch, 'city_image': city_info.image, 'city_description_1': city_info.description[:80], 'city_description_2': city_info.description[80:], 'result': result})


def get_location(location_ids):
    queryset = IgPost.objects.filter(location_id__in=location_ids)
    q = queryset.values_list('location_name', 'owner_id')
    # 計算地標打卡數量，不重複計算同一個帳號的貼文
    owners = set()
    loc_list = []
    for location_name, owner_id in q:
        if owner_id not in owners:
            loc_list.append(location_name)
            owners.add(owner_id)

    loc_map = LocationMap.get_location_map()
    # 同一個地標如果存在不同的打卡標籤，會用相同的名稱做替換
    location = [loc_map[i] if i in loc_map.keys() else i for i in loc_list]
    counter = Counter(location)
    top_loc = [i[0] for i in counter.most_common(5) if i[1]]
    # print(top_loc)
    query = IgLocation.objects.filter(location_name__in=top_loc)
    serializer = IgLocationSerializer(query, many=True)
    res = serializer.data
    loc = set()
    for city in res:
        name = city['location_name']
        if name in top_loc and name not in loc:
            city['rank'] = top_loc.index(name) + 1
            loc.add(name)
    result = [i for i in res if 'rank' in i.keys()]

    return sorted(result, key=lambda x: x['rank'])


def get_top_city(country_name, rank):
    country_trans = {
        "japan": "日本",
        "korea": "韓國",
        "vietnam": "越南",
        "thailand": "泰國",
    }
    queryset = IgPost.objects.filter(counrty=country_trans[country_name], has_location=1).exclude(
        location_city__contains='Taiwan').exclude(location_city__contains='Taoyuan').values_list('location_city', flat=True)
    if country_name == 'japan':
        city = [i.replace(', Japan', '').replace('Shinjuku', 'Shinjuku, Tokyo').split(
            ',')[-1].strip() for i in queryset if i != '']
    elif country_name == 'korea':
        city = [i.replace(', Korea', '').replace(', South Korea', '').split(
            ',')[-1].strip() for i in queryset if i != '']
    elif country_name == 'vietnam':
        city = [i.replace(f', {country_name.title()}', '').replace('Ðà Nẵng', 'Da Nang').replace(
            'Quang Nam-Da Nang', 'Da Nang').split(',')[-1].strip() for i in queryset if i != '']
    elif country_name == 'thailand':
        city = [i.replace(f', {country_name.title()}', '').replace(
            'Phra Nakhon Si Ayutthaya', 'Ayutthaya').split(',')[-1].strip() for i in queryset if i != '']
    counter = Counter(city)
    return counter.most_common(rank)


class CityInfoViewSet(viewsets.ViewSet):
    queryset = CityInfo.objects.all()
    serializer_class = CityInfoSerializer

    @action(['GET'], False)
    def info(self, request, city):
        queryset = CityInfo.objects.get(city_name=city)
        serializer = CityInfoSerializer(queryset)
        res = serializer.data
        res['description_1'] = res['description'][:80]
        res['description_2'] = res['description'][80:]

        return(Response(res))


class TopCityViewSet(mixins.ListModelMixin,
                     GenericViewSet):
    queryset = CityInfo.objects.all()
    serializer_class = CityInfoSerializer

    def list(self, *args, **kwargs):
        country_name = self.kwargs['country']
        country_trans = {
            "japan": "日本",
            "korea": "韓國",
            "vietnam": "越南",
            "thailand": "泰國",
        }

        top_city_counter = get_top_city(country_name, 5)
        top_city = [i[0] for i in top_city_counter]
        query = CityInfo.objects.filter(city_name__in=top_city)
        serializer = CityInfoSerializer(query, many=True)
        res = {}
        res['country_name'] = country_name
        res['country_name_ch'] = country_trans[country_name]
        res['city'] = serializer.data
        for city in res['city']:
            city['rank'] = top_city.index(city['city_name']) + 1
            city['description'] = city['description'][:62]
        res['city'] = sorted(res['city'], key=lambda x: x['rank'])
        return Response(res)


class TopLocationViewSet(mixins.ListModelMixin,
                         GenericViewSet):
    queryset = IgLocation.objects.all()
    serializer_class = IgLocationSerializer

    def list(self, *args, **kwargs):
        city_name = self.kwargs['city']
        query = IgLocation.objects.filter(location_city__icontains=city_name)
        tag_spot_res = query.filter(Q(category='地標和名勝古蹟') | Q(category__in=[
                                    '公園', '國家公園', '河流', '旅遊與交通運輸', '海灘', '橋樑', '島嶼', '峽灣'])).values_list('location_id', flat=True)
        tag_restaurant = query.filter(Q(category__icontains='餐廳') | Q(category__icontains='麵店') | Q(
            category__icontains='燒烤店') | Q(category__in=['壽司店', '三明治店'])).values_list('location_id', flat=True)
        tag_coffee = query.filter(Q(category__icontains='咖啡') | Q(category__icontains='甜點') | Q(
            category__icontains='烘焙') | Q(category__in=['茶店', ])).values_list('location_id', flat=True)
        tag_shopping = query.filter(Q(category__icontains='購物') | Q(category__icontains='市場') | Q(
            category__icontains='商家') | Q(category__in=['雜貨店', ])).values_list('location_id', flat=True)
        tag_fun = query.filter(Q(category__in=['藝術與娛樂', '動物園', '水族館', '博物館', '遊樂主題公園']) | Q(
            category__icontains='美術館')).values_list('location_id', flat=True)

        result = []
        tag_spot_res_res = get_location(tag_spot_res)
        tag_restaurant_res = get_location(tag_restaurant)
        tag_coffee_res = get_location(tag_coffee)
        tag_shopping_res = get_location(tag_shopping)
        tag_fun_res = get_location(tag_fun)

        if tag_spot_res_res:
            result.append({'tag': '觀光景點', 'location': tag_spot_res_res})
        if tag_restaurant_res:
            result.append({'tag': '餐廳', 'location': tag_restaurant_res})
        if tag_coffee_res:
            result.append({'tag': '咖啡廳', 'location': tag_coffee_res})
        if tag_shopping_res:
            result.append({'tag': '逛街', 'location': tag_shopping_res})
        if tag_fun_res:
            result.append({'tag': '休閒', 'location': tag_fun_res})
        return Response(result)
