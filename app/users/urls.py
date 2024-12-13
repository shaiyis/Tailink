from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
]