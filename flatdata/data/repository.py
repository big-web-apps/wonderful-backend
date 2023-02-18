from typing import Dict

from django.db.models import Max, Min
from .models import ApartmentComplex, Flat


class ApartmentComplexRepository:
    @staticmethod
    def get_queryset():
        return ApartmentComplex.objects.all()

    @staticmethod
    def get_object_by_name(name: str):
        return ApartmentComplex.objects.get(name=name)

    @staticmethod
    def insert(data: Dict):
        ApartmentComplex.objects.create(**data)


class FlatRepository:
    @staticmethod
    def get_queryset():
        return Flat.objects.all()

    @staticmethod
    def get_filtered_queryset(query_filters: Dict):
        filters = {
            'square': [Flat.objects.aggregate(Min('square'))['square__min'], Flat.objects.aggregate(Max('square'))['square__max'] + 1],
            'floor': [Flat.objects.aggregate(Min('floor'))['floor__min'], Flat.objects.aggregate(Max('floor'))['floor__max'] + 1],
            'rooms': [Flat.objects.aggregate(Min('rooms'))['rooms__min'], Flat.objects.aggregate(Max('rooms'))['rooms__max'] + 1],
            'districts': list(map(lambda x:x.get('districts'), list(Flat.objects.values('districts').distinct()))),
            'class_type': list(map(lambda x: x.get('class_type'),
                                   list(ApartmentComplex.objects.values('class_type').distinct()))),
            'price': [Flat.objects.aggregate(Min('price'))['price__min'], Flat.objects.aggregate(Max('price'))['price__max'] + 1]
        }
        for param in dict(query_filters):
            try:
                filters[param] = list(map(int, query_filters[param].split('-')))
            except ValueError:
                filters[param] = query_filters[param].split('-')
        return Flat.objects.filter(
            square__range=filters['square'],
            floor__range=filters['floor'],
            rooms__range=filters['rooms'],
            price__range=filters['price'],
            districts__in=filters['districts'],
            apartment_complex__class_type__in=filters['class_type']
        )

    @staticmethod
    def insert(data: Dict):
        Flat.objects.create(**data)

    @staticmethod
    def get_all_regions():
        return list(map(lambda x:x.get('districts'), list(Flat.objects.values('districts').distinct())))
