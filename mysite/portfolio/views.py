from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import AboutMeForm, ExperienceForm, BackgroundForm, ProjectForm
from .models import AboutMe, Experience, Background, Project


def index(request):
    """Index of portfolio app."""
    user = None
    if request.method == "GET":
        user = request.user
        # data = AboutMe.objects.filter(user=user).first()
        experience = Experience.objects.filter(user=user)
        backgrounds = Background.objects.filter(user=user)
        projects = Project.objects.filter(user=user)
        user.experience = experience
        user.backgrounds = backgrounds
        user.projects = projects

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


class AddBackground(CreateView):
    """Create academic background record."""

    model = Background
    form_class = BackgroundForm
    template_name = 'edit_background.html'
    success_url = reverse_lazy('portfolio:index')

    def form_valid(self, form):
        """Validate, add the current user and save the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditBackground(UpdateView):
    """Update academic background record."""

    model = Background
    form_class = BackgroundForm
    template_name = 'edit_background.html'
    success_url = reverse_lazy('portfolio:index')

    def form_valid(self, form):
        """Validate, add the current user and save the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


def delete_background(request, id):
    """Delete 'Academic background' of current user by id."""
    background = get_object_or_404(Background, pk=id)
    background.delete()

    return redirect("portfolio:index")


class AddProject(CreateView):
    """Create Project record."""

    model = Project
    form_class = ProjectForm
    template_name = 'edit_project.html'
    success_url = reverse_lazy('portfolio:index')

    def form_valid(self, form):
        """Validate, add the current user and save the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditProject(UpdateView):
    """Update project record."""

    model = Project
    form_class = ProjectForm
    template_name = 'edit_project.html'
    success_url = reverse_lazy('portfolio:index')

    def form_valid(self, form):
        """Validate, add the current user and save the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


def delete_project(request, id):
    """Delete 'Project' of current user by id."""
    project = get_object_or_404(Project, pk=id)
    project.delete()

    return redirect("portfolio:index")