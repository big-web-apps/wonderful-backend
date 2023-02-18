from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from .repository import ApartmentComplexRepository, FlatRepository
from .serializers import ApartmentComplexSerializer, FlatSerializer

# Create your views here.


class ApartmentComplexViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = ApartmentComplexSerializer
    queryset = ApartmentComplexRepository.get_queryset()


class FlatViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = FlatSerializer
    queryset = FlatRepository.get_queryset()


class FilteredFlatApiView(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    serializer_class = FlatSerializer()

    def get_queryset(self):
        return FlatRepository.get_filtered_queryset(self.request.query_params)

