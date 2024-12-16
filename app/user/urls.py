from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views

router = DefaultRouter()

router.register('profiles', views.ProfileViewSet)

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('register/', views.UserRegisterApiView.as_view()),
    path('', include(router.urls)),
]