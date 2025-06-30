from django.urls import path, include
from rest_framework.routers import DefaultRouter
from owner import views

app_name = 'owner'

router = DefaultRouter()

router.register('owners', views.OwnerViewSet, basename='owners')
router.register('owner-availability', views.OwnerAvailabilityViewSet, basename='owner-availability')
router.register('nearby-owners', views.NearbyOwnersViewSet, basename='nearby-owners')
router.register('dogs', views.DogViewSet, basename='dogs')


urlpatterns = [
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('register/', views.UserRegisterApiView.as_view(), name='register'),
    path('ai-based-match/', views.AIBaseSuggestionView.as_view()),
    path('', include(router.urls)),
]