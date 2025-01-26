from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from . import serializers
from place.models import Place
from .utils import get_place_details

class PlaceViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for viewing places along with their information.
    """
    queryset = Place.objects.all()
    serializer_class = serializers.PlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class CreatePlaceView(APIView):
    def post(self, request):
        place_name = request.data.get("name")
        
        place_data = get_place_details(place_name)
        if not place_data:
            return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
        
        place, created = Place.objects.get_or_create(
            name=place_data["name"],
            defaults={
                "address": place_data["address"],
                "latitude": place_data["latitude"],
                "longitude": place_data["longitude"]
            }
        )

        serializer = serializers.PlaceSerializer(place)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
