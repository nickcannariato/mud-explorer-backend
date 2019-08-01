from django.db import models
from django.contrib.auth.models import User
from mud_explorer.models import Room
import requests


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game_token = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
