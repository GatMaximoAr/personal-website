from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import AboutMeForm, ExperienceForm
from .models import AboutMe, Experience


def index(request):
    """Index of portfolio app."""
    user = None
    if request.method == "GET":
        user = request.user
        # data = AboutMe.objects.filter(user=user).first()
        experience = Experience.objects.filter(user=user)
        user.experience = experience

    return render(request, "index.html", {"data_": user})


class AddAboutMe(CreateView):
    """Create new about me record."""

    model = AboutMe
    form_class = AboutMeForm
    template_name = 'edit_about.html'
    success_url = reverse_lazy('portfolio:index')

    def form_valid(self, form):
        """Validate, add the current user and save the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditAboutMe(UpdateView):
    """Update about me record."""

    model = AboutMe
    form_class = AboutMeForm
    template_name = 'edit_about.html'
    success_url = reverse_lazy('portfolio:index')

    def form_valid(self, form):
        """Validate, add the current user and save the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


def delete_about(request):
    """Delete 'about' of current user."""
    try:
        about_me = AboutMe.objects.get(user=request.user)
        about_me.delete()
    except ObjectDoesNotExist as e:
        print(e)

    return redirect("portfolio:index")


class AddExperience(CreateView):
    """Create new experience record."""

    model = Experience
    form_class = ExperienceForm
    template_name = 'edit_experience.html'
    success_url = reverse_lazy('portfolio:index')

    def form_valid(self, form):
        """Validate, add the current user and save the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditExperience(UpdateView):
    """Update experience record."""

    model = Experience
    form_class = ExperienceForm
    template_name = 'edit_experience.html'
    success_url = reverse_lazy('portfolio:index')

    def form_valid(self, form):
        """Validate, add the current user and save the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


def delete_experience(request, id):
    """Delete 'Experience' of current user by id."""
    experience = get_object_or_404(Experience, pk=id)
    experience.delete()

    return redirect("portfolio:index")