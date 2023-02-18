from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ApartmentComplexViewSet, FlatViewSet


router = DefaultRouter()
router.register(r'apartmentcomplexes', ApartmentComplexViewSet, 'apartmentcomplex')
router.register(r'flats', FlatViewSet, 'flat')
urlpatterns = router.urls
