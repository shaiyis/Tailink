from django.contrib.auth.models import User
import os
from rest_framework import serializers
import requests
from .models import Owner, Dog, OwnerAvailability

class BaseOwnerSerializer(serializers.ModelSerializer):
    # Fields from User model
    first_name = serializers.CharField(source='user.first_name', max_length=30, required=True)
    last_name = serializers.CharField(source='user.last_name', max_length=30, required=True)

    # Fields from Profile model
    gender = serializers.CharField(max_length=20, required=True)
    age = serializers.IntegerField(required=True)
    city = serializers.CharField(max_length=100, required=True)
    about_me = serializers.CharField(required=True)

    class Meta:
        model = Owner
        fields = [
            'first_name', 'last_name',
            'gender', 'age', 'city', 'about_me', 'picture'
        ]


class RegisterSerializer(BaseOwnerSerializer):
    # Fields from User model
    username = serializers.CharField(source='user.username', max_length=30, required=True)
    password = serializers.CharField(source='user.password', write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.CharField(source='user.email', max_length=30, required=True)

    class Meta(BaseOwnerSerializer.Meta):
        fields = ['username', 'password', 'email'] + BaseOwnerSerializer.Meta.fields

    def create(self, validated_data):
        # Extract Profile-specific fields
        owner_data = {
            'gender': validated_data.pop('gender'),
            'age': validated_data.pop('age'),
            'city': validated_data.pop('city'),
            'about_me': validated_data.pop('about_me'),
            'picture': validated_data.get('picture', None)  # Optional field
        }

        # Create User instance
        user = User.objects.create_user(
            username=validated_data['user']['username'],
            password=validated_data['user']['password'],
            email=validated_data['user']['email'],
            first_name=validated_data['user']['first_name'],
            last_name=validated_data['user']['last_name']
        )

        # Create Profile instance
        owner = Owner.objects.create(user=user, **owner_data)        
        owner.save()

        return user


PLACE_SERVICE_URL = os.environ.get("PLACE_SERVICE_URL", "http://localhost:8000/api/place/")

class OwnerAvailabilitySerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(write_only=True)  # Accept owner_username in input
    dog = serializers.CharField(write_only=True)
    place_name = serializers.CharField(write_only=True)  # Accept place_name in input
    place_id = serializers.UUIDField(read_only=True)  # Store UUID but hide it from input
    start_time = serializers.DateTimeField(required=True)
    end_time = serializers.DateTimeField(required=True)

    class Meta:
        model = OwnerAvailability
        # fields = '__all__'  # Include all fields in the model
        fields = ['owner_username', 'dog', 'place_name', 'place_id', 'start_time', 'end_time']

    def create(self, validated_data):
        """Manually retrieve Owner and Place ID before saving"""

        # Extract owner_username & place_name from validated_data
        owner_username = validated_data.pop('owner_username')
        dog = validated_data.pop('dog')
        place_name = validated_data.pop('place_name')

        # Get Owner object
        owner = Owner.objects.filter(user__username=owner_username).first()
        if not owner:
            raise serializers.ValidationError({'owner_username': 'Owner not found'})
        
        # Get Dog object
        dog_instance = Dog.objects.filter(owner=owner, name=dog).first()
        if not dog_instance:
            raise serializers.ValidationError({'dog': 'Dog not found for this owner'})

        # Fetch place_id from Place Service API
        response = requests.get(f"{PLACE_SERVICE_URL}places?name={place_name}")

        print(f"Using PLACE_SERVICE_URL: {PLACE_SERVICE_URL}", flush=True) # Debugging
        print(f"place_name: {place_name}", flush=True) # Debugging
        print(f"response: {response}", flush=True) # Debugging

        if response.status_code == 200 and response.json():
            place_id = response.json()[0]['id']  # Extract place_id from API response
        else:
            raise serializers.ValidationError({'place_name': 'Place not found in Place Service'})

        # Now create ProfileAvailability (without profile_username & place_name)
        return OwnerAvailability.objects.create(
            owner=owner,
            dog=dog_instance,
            place_id=place_id,  # Store UUID
            **validated_data  # Includes start_time & end_time
        )


    def to_representation(self, instance):
        """Fetch place_name from Place Service using place_id"""
        data = super().to_representation(instance)

        data['owner_username'] = instance.owner.user.username
        data['dog'] = instance.dog.name

        # Call the Place Service API to get place_name
        response = requests.get(f"{PLACE_SERVICE_URL}places/{instance.place_id}/")
        if response.status_code == 200:
            data['place_name'] = response.json().get('name', 'Unknown')
        else:
            data['place_name'] = 'Unknown'

        return data


class DogSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(write_only=True) # Comment so it will be included in the output
    breed = serializers.CharField(write_only=True)  # Accept place_name in input
    age = serializers.IntegerField(required=True)
    about = serializers.CharField(write_only=True)

    class Meta:
        model = Dog
        # fields = '__all__'  # Include all fields in the model
        fields = ['name', 'breed', 'age', 'about', 'picture']

    def create(self, validated_data):
        # Extract owner_username & place_name from validated_data
        # owner_username = validated_data.pop('owner_username')

        user = self.context['request'].user

        '''
        # Get Owner object
        owner = Owner.objects.filter(user__username=owner_username).first()
        if not owner:
            raise serializers.ValidationError({'owner_username': 'Owner not found'})
        '''
        # Get the Owner object linked to the user
        try:
            owner = user.owner
        except Owner.DoesNotExist:
            raise serializers.ValidationError("Owner profile not found for this user.")

        # Now create Dog instance
        return Dog.objects.create(
            owner=owner,
            **validated_data
        )
