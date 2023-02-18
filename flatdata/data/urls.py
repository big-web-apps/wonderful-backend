from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ApartmentComplexViewSet, FlatViewSet, FilteredFlatApiView, GetApiApartmentsComplexesApiView, GetApiFlatsApiView, GetAllRegionsApiView


router = DefaultRouter()
router.register(r'apartmentcomplexes', ApartmentComplexViewSet, 'apartmentcomplex')
router.register(r'flats', FlatViewSet, 'flat')
urlpatterns = [
    path('filteredflats/', FilteredFlatApiView.as_view()),
    path('loadaparts/', GetApiApartmentsComplexesApiView.as_view()),
    path('loadflats/', GetApiFlatsApiView.as_view()),
    path('getallregions/', GetAllRegionsApiView.as_view()),
]
urlpatterns += router.urls
