from rest_framework import serializers
from .models import Place

class PlaceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20, required=True)
    address = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Place
        fields = ['id', 'name', 'address']
