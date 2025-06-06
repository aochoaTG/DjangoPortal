"""Profile model for the accounts app."""
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Profile model for the accounts app."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"  # pylint: disable=no-member
