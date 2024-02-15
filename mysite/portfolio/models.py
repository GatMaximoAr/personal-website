from django.db import models
from django.contrib.auth.models import User


class AboutMe(models.Model):
    """Abstract class 'About me' of Django ORM."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    about = models.TextField(null=False)
    picture = models.ImageField(upload_to="profile_picture/", null=False)

    def __str__(self):
        """Model str representation."""
        return f"firstname={self.firstname}, lastname={self.lastname}," \
               f" about={self.about}, picture={self.picture}"


class Experience(models.Model):
    """Abstract class 'Experience' of Django ORM."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.CharField(max_length=100, null=False)
    description = models.TextField()
    start_date = models.DateField(null=False)
    finish_date = models.DateField()
    current = models.BooleanField()
    link_info = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="experience_picture/", null=False)

    def __str__(self):
        """Model str representation."""
        return f"job={self.job}, description={self.description}, start_date={self.start_date}," \
               f" finish_date={self.finish_date}, current={self.current}, " \
               f" link_info={self.link_info}, picture={self.picture}"


class Background(models.Model):
    """Abstract class 'Academic background' of Django ORM."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    institution = models.CharField(max_length=150, null=False)
    degree = models.CharField(max_length=50, null=False)
    start_date = models.DateField(null=False)
    finish_date = models.DateField()
    link_info = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="background_picture/", null=False)

    def __str__(self):
        """Model str representation."""
        return f"title={self.title}, institution={self.institution}, degree={self.degree}," \
               f" start_date={self.start_date}, finish_date={self.finish_date}, " \
               f" link_info={self.link_info}, picture={self.picture}"