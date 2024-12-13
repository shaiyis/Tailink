from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# input username, password, output - AuthToken
class UserLoginApiView(ObtainAuthToken):
   """Handle creating user authentication tokens"""
   renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES