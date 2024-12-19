from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Hobby, ProfileAvailability


class BaseProfileSerializer(serializers.ModelSerializer):
    # Fields from User model
    first_name = serializers.CharField(source='user.first_name', max_length=30, required=True)
    last_name = serializers.CharField(source='user.last_name', max_length=30, required=True)

    # Fields from Profile model
    age = serializers.IntegerField(required=True)
    city = serializers.CharField(max_length=100, required=True)
    about_me = serializers.CharField(required=True)
    looking_for = serializers.CharField(required=True)
    picture = serializers.CharField(max_length=100,required=False)
    hobbies = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Hobby.objects.all(), required=False
    )

    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name',
            'age', 'city', 'about_me', 'looking_for', 'picture', 'hobbies'
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


class ProfileAvailabilitySerializer(serializers.ModelSerializer):
    profile_first_name = serializers.CharField(source='profile.user.first_name', max_length=30, required=True)
    profile_last_name = serializers.CharField(source='profile.user.last_name', max_length=30, required=True)
    place_name = serializers.CharField(source='place.name', max_length=30, required=True)

    class Meta:
        model = ProfileAvailability
        #fields = '__all__'  # Include all fields in the model
        fields = ['profile_first_name', 'profile_last_name', 'place_name', 'start_time', 'end_time']
