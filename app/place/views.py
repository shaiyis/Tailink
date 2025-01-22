from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet
from . import serializers
from place.models import Place

class PlaceViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for viewing places along with their information.
    """
    queryset = Place.objects.all()
    serializer_class = serializers.PlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

