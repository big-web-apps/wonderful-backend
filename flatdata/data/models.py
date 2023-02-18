from django.db import models

# Create your models here.


class ApartmentComplex(models.Model):
    name = models.CharField(max_length=64)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    class_type = models.CharField(max_length=16)
    image = models.ImageField(upload_to='images/complexes/')


class Flat(models.Model):
    apartment_complex = models.ForeignKey(ApartmentComplex, on_delete=models.CASCADE)
    rooms = models.IntegerField()
    floor = models.IntegerField()
    liter_name = models.CharField(max_length=32)
    districts = models.CharField(max_length=32)
    meter_price = models.IntegerField()
    price = models.IntegerField()
    sale_price = models.IntegerField(null=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/flats/')
    square = models.FloatField()
    living_square = models.FloatField()
    coefficient = models.FloatField(default=0)
