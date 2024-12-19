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
    

class ProfileAvailability(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    place = models.OneToOneField('place.Place', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return (
            f"{self.profile} is available at {self.place} "
            f"from {self.start_time.strftime('%Y-%m-%d %H:%M')} "
            f"to {self.end_time.strftime('%Y-%m-%d %H:%M')}"
        )


