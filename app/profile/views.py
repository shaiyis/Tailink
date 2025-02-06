from django.conf import settings
from django.db.models import F
from django.db.models.functions import Abs
from django_filters.rest_framework import DjangoFilterBackend
from math import radians, cos, sin, asin, sqrt
import openai
from profile.models import Profile, ProfileAvailability
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from . import serializers
from .utils import get_current_location


# input username, password, output - AuthToken
class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        # Authenticate user and get token
        response = super().post(request, *args, **kwargs)
        token = response.data.get("token")

        if token:
            user = Token.objects.get(key=token).user
            self.update_user_location(user)  # Call the location update function

        return response

    def update_user_location(self, user):
        """Update user's location when they log in"""
        
        location = get_current_location()
        if location:
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.latitude = location["latitude"]
            profile.longitude = location["longitude"]
            profile.save()


class UserRegisterApiView(APIView):
    """Handle registering profiles"""
    serializer_class = serializers.RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
               {'message': 'User registered successfully!'},
               status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProfileViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for viewing profiles along with user information.
    """
    queryset = Profile.objects.select_related('user').all()
    serializer_class = serializers.BaseProfileSerializer


class ProfileMatchesViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for viewing profiles matches:
    Age difference is up to 5 years and the profiles have at least one hobby in common.
    """
    authentication_classes = (TokenAuthentication,)  # Use Token-based authentication
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get_queryset(self):
        # Get the current user's profile
        user_profile = Profile.objects.filter(user=self.request.user).first()

        if not user_profile:
            return Response({"error": "Profile not found for the current user"}, status=404)
        
        # Get profiles with age difference up to 5 and at least one hobby in common
        return Profile.objects.annotate(
            age_difference=Abs(F('age') - user_profile.age)
        ).filter(
            age_difference__lte=5,
            hobbies__in=user_profile.hobbies.all()
        ).exclude(
            id=user_profile.id  # Exclude the current user's profile
        ).exclude(
            gender=user_profile.gender  # Exclude profiles with the same gender
        ).distinct()  # Ensure no duplicates due to ManyToMany relationships

    def list(self, request):
        matches = self.get_queryset()
        serializer = serializers.BaseProfileSerializer(matches, many=True)
        # Return the matching profiles
        return Response(serializer.data)
    

class ProfileAvailabilityViewSet(ModelViewSet):
    """
    ViewSet for viewing and managing profile availability.
    """
    queryset = ProfileAvailability.objects.all()
    serializer_class = serializers.ProfileAvailabilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['profile', 'place_id', 'start_time', 'end_time']


class NearbyProfilesViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for viewing profiles near the current profile.
    """
    authentication_classes = (TokenAuthentication,)  # Use Token-based authentication
    permission_classes = [IsAuthenticated]

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        return R * c

    def get_queryset(self):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)

        if not user_profile or user_profile.latitude is None or user_profile.longitude is None:
            return Profile.objects.none()  # No location data

        user_lat, user_lon = user_profile.latitude, user_profile.longitude

        # Get radius from query params (default is 10 km)
        radius_km = float(self.request.query_params.get("radius", 10))

        nearby_profiles = []
        for profile in Profile.objects.exclude(user=user):
            if profile.latitude is not None and profile.longitude is not None:
                distance = NearbyProfilesViewSet.haversine_distance(
                    user_lat, user_lon, profile.latitude, profile.longitude)
                if distance <= radius_km:
                    nearby_profiles.append(profile)
        
        return nearby_profiles

    def list(self, request):
        nearby_profiles = self.get_queryset()
        serializer = serializers.BaseProfileSerializer(nearby_profiles, many=True)
        return Response(serializer.data)
    

class AIBaseSuggestionView(APIView):
    """
    View for AI-based suggestions for profile matches.
    """
    authentication_classes = (TokenAuthentication,)  # Use Token-based authentication
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_profile = Profile.objects.filter(user=request.user).first()

        if not user_profile:
            return Response({"error": "Profile not found"}, status=404)

        # Reuse the match logic from ProfileMatchesViewSet
        viewset = ProfileMatchesViewSet()
        viewset.request = request
        matches = viewset.get_queryset()

        if not matches.exists():
            return Response({"message": "No suitable matches found."}, status=200)

        serializer = serializers.BaseProfileSerializer(matches, many=True)
        profiles_data = serializer.data
        
        match_strings = "".join([
            f"- Name: {match['first_name']} {match['last_name']}, Age: {match['age']}, "
            f"Gender: {match['gender']}, City: {match['city']}\n"
            f"  About: {match['about_me']}\n"
            f"  Looking for: {match['looking_for']}\n"
            f"  Hobbies: {', '.join(match['hobbies'])}\n"
            for match in profiles_data
            ])

        # Prepare AI prompt
        prompt = (
            f"You are an AI matchmaker helping users find a compatible match.\n"
            f"The user profile is:\n"
            f"Name: {user_profile.user.first_name} {user_profile.user.last_name},\n"
            f"Age: {user_profile.age}, Gender: {user_profile.gender}, "
            f"City: {user_profile.city}\n"
            f"About: {user_profile.about_me}\n"
            f"Looking for: {user_profile.looking_for}\n"
            f"Hobbies: {', '.join(hobby.name for hobby in user_profile.hobbies.all())}\n"
            f"Here are potential matches:\n{match_strings}"
            f"Based on age compatibility and shared interests, suggest the best match and explain why."
        )

        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert relationship matchmaker."},
                    {"role": "user", "content": prompt}
                ]
            )
            suggestion = response.choices[0].message.content
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({"suggestion": suggestion})
