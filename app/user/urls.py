from django.urls import path
from user import views
from django.http import HttpResponse


urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('register/', views.UserRegisterApiView.as_view()),
]