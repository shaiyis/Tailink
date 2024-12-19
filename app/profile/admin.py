from django.contrib import admin
from profile import models

admin.site.register(models.Hobby)
admin.site.register(models.Profile)
admin.site.register(models.ProfileAvailability)


