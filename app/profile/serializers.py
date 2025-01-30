from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Hobby, ProfileAvailability
import requests

class BaseProfileSerializer(serializers.ModelSerializer):
    # Fields from User model
    first_name = serializers.CharField(source='user.first_name', max_length=30, required=True)
    last_name = serializers.CharField(source='user.last_name', max_length=30, required=True)

    # Fields from Profile model
    gender = serializers.CharField(max_length=20, required=True)
    age = serializers.IntegerField(required=True)
    city = serializers.CharField(max_length=100, required=True)
    about_me = serializers.CharField(required=True)
    looking_for = serializers.CharField(required=True)
    picture = serializers.CharField(max_length=100,required=False)
    hobbies = serializers.StringRelatedField(many=True)
    '''
    hobbies = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Hobby.objects.all(), required=False
    )
    '''

    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name',
            'gender', 'age', 'city', 'about_me', 'looking_for', 'picture', 'hobbies'
        ]


class RegisterSerializer(BaseProfileSerializer):
    # Fields from User model
    username = serializers.CharField(source='user.username', max_length=30, required=True)
    password = serializers.CharField(source='user.password', write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.CharField(source='user.email', max_length=30, required=True)

    class Meta(BaseProfileSerializer.Meta):
        fields = ['username', 'password', 'email'] + BaseProfileSerializer.Meta.fields

    def create(self, validated_data):
        # Extract Profile-specific fields
        profile_data = {
            'gender': validated_data.pop('gender'),
            'age': validated_data.pop('age'),
            'city': validated_data.pop('city'),
            'about_me': validated_data.pop('about_me'),
            'looking_for': validated_data.pop('looking_for'),
            'picture': validated_data.pop('picture', None)
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
        profile = Profile.objects.create(user=user, **profile_data)

        hobbies = validated_data.pop('hobbies', [])
        if hobbies:
            profile.hobbies.set(hobbies)  # Many-to-Many relationship
        
        profile.save()

        return user


PLACE_SERVICE_URL = "http://localhost:8000/api/place/"

class ProfileAvailabilitySerializer(serializers.ModelSerializer):
    profile_username = serializers.CharField(write_only=True)  # Accept profile_username in input
    place_name = serializers.CharField(write_only=True)  # Accept place_name in input
    place_id = serializers.UUIDField(read_only=True)  # Store UUID but hide it from input
    start_time = serializers.DateTimeField(required=True)
    end_time = serializers.DateTimeField(required=True)

    class Meta:
        model = ProfileAvailability
        #fields = '__all__'  # Include all fields in the model
        fields = ['profile_username', 'place_name', 'place_id', 'start_time', 'end_time']

    def create(self, validated_data):
        """Manually retrieve Profile and Place ID before saving"""

        # Extract profile_username & place_name from validated_data
        profile_username = validated_data.pop('profile_username')
        place_name = validated_data.pop('place_name')

        # Get Profile object
        profile = Profile.objects.filter(user__username=profile_username).first()
        if not profile:
            raise serializers.ValidationError({'profile_username': 'Profile not found'})

        # Fetch place_id from Place Service API
        response = requests.get(f"{PLACE_SERVICE_URL}places?name={place_name}")
        if response.status_code == 200 and response.json():
            place_id = response.json()[0]['id']  # Extract place_id from API response
        else:
            raise serializers.ValidationError({'place_name': 'Place not found in Place Service'})

        # Now create ProfileAvailability (without profile_username & place_name)
        return ProfileAvailability.objects.create(
            profile=profile,
            place_id=place_id,  # Store UUID
            **validated_data  # Includes start_time & end_time
        )


    def to_representation(self, instance):
        """Fetch place_name from Place Service using place_id"""
        data = super().to_representation(instance)

        data['profile_username'] = instance.profile.user.username

        # Call the Place Service API to get place_name
        response = requests.get(f"{PLACE_SERVICE_URL}places/{instance.place_id}/")
        if response.status_code == 200:
            data['place_name'] = response.json().get('name', 'Unknown')
        else:
            data['place_name'] = 'Unknown'

        return data
