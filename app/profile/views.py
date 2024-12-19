from django.db.models import F
from django.db.models.functions import Abs
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from . import serializers
from profile.models import Profile, ProfileAvailability


# input username, password, output - AuthToken
class UserLoginApiView(ObtainAuthToken):
   """Handle creating user authentication tokens"""
   renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserRegisterApiView(APIView):
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
        ).distinct()  # Ensure no duplicates due to ManyToMany relationships

    def list(self, request):
        matches = self.get_queryset()
        serializer = serializers.BaseProfileSerializer(matches, many=True)
        # Return the matching profiles
        return Response(serializer.data)
    

class ProfileAvailabilityViewSet(ModelViewSet):
    queryset = ProfileAvailability.objects.select_related('profile').select_related('place').all()
    serializer_class = serializers.ProfileAvailabilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['profile', 'place', 'start_time', 'end_time']