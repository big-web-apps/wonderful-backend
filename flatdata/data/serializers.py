from rest_framework import serializers

from .models import ApartmentComplex, Flat


class ApartmentComplexSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApartmentComplex
        fields = '__all__'


class FlatSerializer(serializers.ModelSerializer):
    apartment_complex = ApartmentComplexSerializer()

    class Meta:
        model = Flat
        fields = '__all__'
