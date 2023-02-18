import requests

from django.conf import settings

from flatdata.celery import app
from .repository import ApartmentComplexRepository, FlatRepository
from .serializers import FlatSerializer


@app.task
def update_coefficients():
    for obj in FlatRepository.get_queryset():
        response = requests.post(settings.ANALYTIC_SYSTEM_URL, data=FlatSerializer(data=obj).data)
        obj.coefficient = response.json()['coefficient']
        obj.save(updated_fields=['coefficient'])


@app.task
def get_flats_from_api(url):
    data = requests.get(url).json()
    for obj in data['data']['ITEMS']:
        FlatRepository.insert({
            'apartment_complex': ApartmentComplexRepository.get_object_by_name(obj['OBJECT']),
            'rooms': obj['ROOMS'],
            'floor': obj['FLOOR_NUMBER'],
            'liter_name': obj['LITER_NAME'],
            'districts': obj['DISCTRICTS'],
            'meter_price': obj['METER_PRICE'],
            'price': obj['FULL_PRICE'],
            'sale_price': obj['SALE_PRICE'],
            'url': settings.BASE_FLAT_API + obj['DETAIL_PAGE_URL'],
            'image': obj['PICTURE'],
            'square': obj['SQUARE'][0],
            'living_square': obj['LIVING'][0]
        })


@app.task
def get_apartment_complexes_from_api(url: str):
    data = requests.get(url).json()
    for obj in data['filters']['items']:
        ApartmentComplexRepository.insert({
            'name': obj['name'],
            'address': obj['address'],
            'latitude': obj['position'][0],
            'longitude': obj['position'][1],
            'class_type': obj['class'],
            'image': obj['image']
        })

