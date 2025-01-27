from django.contrib.auth.models import User
from django.db import models

class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, default='unspecified')
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    about_me = models.TextField()
    looking_for = models.TextField()
    picture = models.CharField(max_length=100)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.user.username


class ProfileAvailability(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    place_id = models.BigIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return (
            f"{self.profile} is available at place_id {self.place_id} "
            f"from {self.start_time.strftime('%Y-%m-%d %H:%M')} "
            f"to {self.end_time.strftime('%Y-%m-%d %H:%M')}"
        )
