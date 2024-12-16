from django.contrib.auth.models import User
from django.db import models


class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    about_me = models.TextField()
    looking_for = models.TextField()
    picture = models.CharField(max_length=100)
    hobbies = models.ManyToManyField(Hobby, blank=True)

    def __str__(self):
        return self.user.username
