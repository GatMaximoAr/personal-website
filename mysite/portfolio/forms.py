from django import forms
from .models import AboutMe


class AboutMeForm(forms.ModelForm):
    """Abstract class of Django forms."""

    firstname = forms.CharField(max_length=50, required=True, label="First name")
    lastname = forms.CharField(max_length=50, required=True, label="Last name")
    about = forms.CharField(widget=forms.Textarea, label="About")
    picture = forms.FileField(label="Picture")

    class Meta:
        """Meta form class."""

        model = AboutMe
        fields = ["firstname", "lastname", "about", "picture"]