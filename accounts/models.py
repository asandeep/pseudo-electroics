from django.contrib.auth import models as auth_models
from django.db import models
from django.urls import reverse


class User(auth_models.AbstractUser):
    """Extends default model to add project specific fields."""

    birth_date = models.DateField(help_text="Employee Date of birth.")
    address = models.TextField(help_text="Employee permanent address")
    locked = models.BooleanField(
        default=False,
        help_text="Whether the account has been locked by Store owner.",
    )
