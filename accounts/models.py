from django.contrib.auth import models as auth_models
from django.db import models
from django.urls import reverse


class User(auth_models.AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    locked = models.BooleanField(default=False)
