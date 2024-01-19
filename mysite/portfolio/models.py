from django.db import models
from django.contrib.auth.models import User


class AboutMe(models.Model):
    """Abstract class of Django ORM."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    about = models.TextField(null=False)
    picture = models.ImageField(upload_to="profile_picture/", null=False)

    def __str__(self):
        """Model representation."""
        return f"firstname={self.firstname}, lastname={self.lastname}," \
               f" about={self.about}, picture={self.picture}"