from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user import serializers
from user.models import Profile


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
    A simple ViewSet for viewing profiles along with user information.
    """
    queryset = Profile.objects.select_related('user').all()
    serializer_class = serializers.BaseProfileSerializer
