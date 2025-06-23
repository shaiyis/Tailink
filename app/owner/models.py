from django.contrib.auth.models import User
from django.db import models


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, default='unspecified')
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    about_me = models.TextField()
    picture = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Dog(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='dogs')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)  # free-text, e.g., “Golden Retriever”
    age = models.PositiveIntegerField()
    about = models.TextField(blank=True)
    picture = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.breed})"


class OwnerAvailability(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    place_id = models.BigIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return (
            f"{self.owner} is available at place_id {self.place_id}"
            f" with {self.dog}"
            f" from {self.start_time.strftime('%Y-%m-%d %H:%M')}"
            f" to {self.end_time.strftime('%Y-%m-%d %H:%M')}"
        )