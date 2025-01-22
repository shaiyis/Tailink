from django.urls import path, include
from rest_framework.routers import DefaultRouter
from place import views

router = DefaultRouter()

router.register('places', views.PlaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
