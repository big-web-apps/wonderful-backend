from django.contrib import admin

from .models import Flat, ApartmentComplex

# Register your models here.


admin.site.register(ApartmentComplex)
admin.site.register(Flat)