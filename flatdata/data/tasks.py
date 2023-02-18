import requests

from django.conf import settings
from django.core.files import File

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
        if data['data'].get('IS_CORRECT', True):
            img = requests.get(settings.BASE_FLAT_API + obj['PICTURE'][1:])
            with open(obj['DETAIL_PAGE_URL'][12:-1] + '.jpg', 'wb') as f:
                f.write(img.content)
            with open(obj['DETAIL_PAGE_URL'][12:-1] + '.jpg', 'rb') as f:
                django_file = File(f)
                FlatRepository.insert({
                    'apartment_complex': ApartmentComplexRepository.get_object_by_name(obj['OBJECT']),
                    'rooms': obj['ROOMS_COUNT'],
                    'floor': obj['FLOOR_NUMBER'],
                    'liter_name': obj['LITER_NAME'],
                    'districts': obj['DISTRICTS'],
                    'meter_price': obj['METER_PRICE'],
                    'price': obj['FULL_PRICE'],
                    'sale_price': obj['SALE_PRICE'],
                    'url': settings.BASE_FLAT_API + obj['DETAIL_PAGE_URL'][1:],
                    'image': django_file,
                    'square': obj['SQUARE'][0],
                    'living_square': obj['LIVING'][0]
                })


@app.task
def get_apartment_complexes_from_api(url: str):
    data = requests.get(url).json()
    for obj in data['filters']['items']:
        img = requests.get(settings.BASE_FLAT_API + obj['image'][1:])
        with open(obj['name'] + '.jpg', 'wb') as f:
            f.write(img.content)
        with open(obj['name'] + '.jpg', 'rb') as f:
            django_file = File(f)
            ApartmentComplexRepository.insert({
                'name': obj['name'],
                'address': obj['address'],
                'latitude': obj['position'][0],
                'longitude': obj['position'][1],
                'class_type': obj['class'],
                'image': django_file
            })

