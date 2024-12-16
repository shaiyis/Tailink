from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Hobby


class RegisterSerializer(serializers.ModelSerializer):
    print("RegisterSerializer - debug")
    # Fields from User model
    username = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.CharField(max_length=30, required=True)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    # Fields from Profile model
    age = serializers.IntegerField(required=True)
    city = serializers.CharField(max_length=100, required=True)
    about_me = serializers.CharField(required=True)
    looking_for = serializers.CharField(required=True)
    picture = serializers.CharField(max_length=100,required=False)
    #hobbies = serializers.PrimaryKeyRelatedField(
    #    many=True, queryset=Hobby.objects.all(), required=False
    #)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name', 
            'age', 'city', 'about_me', 'looking_for', 'picture'#, 'hobbies'
        ]

    def create(self, validated_data):
        # Extract Profile-specific fields
        profile_data = {
            'age': validated_data.pop('age'),
            'city': validated_data.pop('city'),
            'about_me': validated_data.pop('about_me'),
            'looking_for': validated_data.pop('looking_for'),
            'picture': validated_data.pop('picture', None),
            #'hobbies': validated_data.pop('hobbies', [])
        }

        # Create User instance
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        # Create Profile instance
        profile = Profile.objects.create(user=user, **profile_data)
        #if profile_data['hobbies']:
        #    profile.hobbies.set(profile_data['hobbies'])  # Many-to-Many relationship
        profile.save()

        return user
