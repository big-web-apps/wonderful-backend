from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .repository import ApartmentComplexRepository, FlatRepository
from .serializers import ApartmentComplexSerializer, FlatSerializer
from .tasks import get_apartment_complexes_from_api, get_flats_from_api, update_coefficients

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
    serializer_class = FlatSerializer

    def get_queryset(self):
        return FlatRepository.get_filtered_queryset(self.request.query_params)


class GetApiFlatsApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        get_flats_from_api.apply_async((request.data['url'],))
        return Response(status=status.HTTP_201_CREATED)


class GetApiApartmentsComplexesApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        get_apartment_complexes_from_api.apply_async((request.data['url'],))
        return Response(status=status.HTTP_201_CREATED)


class GetAllRegionsApiView(APIView):

    def get(self, request):
        return Response(FlatRepository.get_all_regions(), status=status.HTTP_200_OK)
