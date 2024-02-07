from django import forms
from .models import AboutMe, Experience


class AboutMeForm(forms.ModelForm):
    """Abstract class 'About me' of Django forms."""

    firstname = forms.CharField(max_length=50, required=True, label="First name")
    lastname = forms.CharField(max_length=50, required=True, label="Last name")
    about = forms.CharField(widget=forms.Textarea, label="About")
    picture = forms.FileField(label="Picture")

    class Meta:
        """Meta form class."""

        model = AboutMe
        fields = ["firstname", "lastname", "about", "picture"]


class ExperienceForm(forms.ModelForm):
    """Abstract class 'Experience' of Django forms."""

    job = forms.CharField(max_length=100, required=True, label="Job")
    description = forms.CharField(widget=forms.Textarea, label="Description", required=True)
    start_date = forms.DateField(required=True, label="Start date")
    finish_date = forms.DateField(label="Finish date")
    current = forms.BooleanField(label="Current", initial=False, required=False)
    link_info = forms.CharField(max_length=100, label="Link")
    picture = forms.FileField(label="Picture", required=True)

    class Meta:
        """Meta form class."""

        model = Experience
        fields = ["job", "description", "start_date", "finish_date",
                  "current", "link_info", "picture"]