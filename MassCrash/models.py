from django.db import models


class User(models.Model):
    email = models.EmailField()
    location = models.CharField(max_length=255)

    class Meta:
        app_label = 'MassCrash'
