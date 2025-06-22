from django.contrib import admin
from owner import models

admin.site.register(models.Dog)
admin.site.register(models.Owner)
admin.site.register(models.OwnerAvailability)