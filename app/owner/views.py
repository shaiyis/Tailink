from django.conf import settings
from django.db.models import F
from django.db.models.functions import Abs
from django_filters.rest_framework import DjangoFilterBackend
from math import radians, cos, sin, asin, sqrt
# import openai # type: ignore
from owner.models import Owner, OwnerAvailability, Dog
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
            owner, _ = Owner.objects.get_or_create(user=user)
            owner.latitude = location["latitude"]
            owner.longitude = location["longitude"]
            owner.save()


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


class OwnerViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for viewing profiles along with user information.
    """
    queryset = Owner.objects.select_related('user').all()
    serializer_class = serializers.BaseOwnerSerializer
    

class OwnerAvailabilityViewSet(ModelViewSet):
    """
    ViewSet for viewing and managing owner availability.
    """
    queryset = OwnerAvailability.objects.all()
    serializer_class = serializers.OwnerAvailabilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner', 'place_id', 'dog', 'start_time', 'end_time']


class NearbyOwnersViewSet(ReadOnlyModelViewSet):
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
        user_owner = Owner.objects.get(user=user)

        if not user_owner or user_owner.latitude is None or user_owner.longitude is None:
            return Owner.objects.none()  # No location data

        user_lat, user_lon = user_owner.latitude, user_owner.longitude

        # Get radius from query params (default is 10 km)
        radius_km = float(self.request.query_params.get("radius", 10))

        nearby_owners = []
        for owner in Owner.objects.exclude(user=user):
            if owner.latitude is not None and owner.longitude is not None:
                distance = NearbyOwnersViewSet.haversine_distance(
                    user_lat, user_lon, owner.latitude, owner.longitude)
                if distance <= radius_km:
                    nearby_owners.append(owner)
        
        return nearby_owners

    def list(self, request):
        nearby_profiles = self.get_queryset()
        serializer = serializers.BaseOwnerSerializer(nearby_profiles, many=True)
        return Response(serializer.data)
    

class AIBaseSuggestionView(APIView):
    """
    View for AI-based suggestions for profile matches.
    """
    authentication_classes = (TokenAuthentication,)  # Use Token-based authentication
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_owner = Owner.objects.filter(user=request.user).first()

        if not user_owner:
            return Response({"error": "Owner not found"}, status=404)

        # Reuse the match logic from ProfileMatchesViewSet
        #viewset = OwnerMatchesViewSet()
        viewset = "todo"
        viewset.request = request
        matches = viewset.get_queryset()

        if not matches.exists():
            return Response({"message": "No suitable matches found."}, status=200)

        serializer = serializers.BaseOwnerSerializer(matches, many=True)
        profiles_data = serializer.data
        
        match_strings = "".join([
            f"- Name: {match['first_name']} {match['last_name']}, Age: {match['age']}, "
            f"Gender: {match['gender']}, City: {match['city']}\n"
            f"  About: {match['about_me']}\n"
            for match in profiles_data
            ])

        # Prepare AI prompt
        prompt = (
            f"You are an AI matchmaker helping users find a compatible match.\n"
            f"The user profile is:\n"
            f"Name: {user_owner.user.first_name} {user_owner.user.last_name},\n"
            f"Age: {user_owner.age}, Gender: {user_owner.gender}, "
            f"City: {user_owner.city}\n"
            f"About: {user_owner.about_me}\n"
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

class DogViewSet(ModelViewSet):
    """
    ViewSet for viewing and managing Dog.
    """
    authentication_classes = (TokenAuthentication,)  # Use Token-based authentication
    permission_classes = [IsAuthenticated]

    queryset = Dog.objects.all()
    serializer_class = serializers.DogSerializer