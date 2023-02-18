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
            'square': [Flat.objects.aggregate(Min('square')), Flat.objects.aggregate(Max('square')) + 1],
            'floor': [Flat.objects.aggregate(Min('floor')), Flat.objects.aggregate(Max('floor')) + 1],
            'rooms': [Flat.objects.aggregate(Min('rooms')), Flat.objects.aggregate(Max('rooms')) + 1],
            'districts': list(map(lambda x: x.get('district'), list(Flat.objects.values('district')))),
            'class_type': list(map(lambda x: x.get('apartment_complex__class_type'),
                                   list(Flat.objects.values('apartment_complex__class_type')))),
            'price': [Flat.objects.aggregate(Min('price')), Flat.objects.aggregate(Max('price')) + 1]
        }
        for param in query_filters:
            filters[param] = query_filters[param]
        return Flat.objects.filter(
            square__range=filters['square'],
            floor_range=filters['floor'],
            rooms_range=filters['rooms'],
            price_range=filters['price'],
            district__in=filters['districts'],
            apartment_complex__class_type=filters['apartment_complex__class_type']
        )

    @staticmethod
    def insert(data: Dict):
        Flat.objects.create(**data)
