from django.shortcuts import render, redirect, get_object_or_404
from .forms import AboutMeForm, ExperienceForm
from .models import AboutMe, Experience
from django.core.exceptions import ObjectDoesNotExist
# from django.http import HttpResponse


def index(request):
    """Index of portfolio app."""
    user = None
    if request.method == "GET":
        user = request.user
        # data = AboutMe.objects.filter(user=user).first()
        experience = Experience.objects.filter(user=user)
        user.experience = experience

    return render(request, "index.html", {"data_": user})


def edit_about(request):
    """Edit about page view."""
    if request.method == "GET":
        form = AboutMeForm()
        try:
            about_me = AboutMe.objects.get(user=request.user)
            form = AboutMeForm(instance=about_me)
        except ObjectDoesNotExist as e:
            print(e)

    elif request.method == "POST":
        try:
            about_me = AboutMe.objects.get(user=request.user)
            form = AboutMeForm(request.POST, request.FILES, instance=about_me)
        except ObjectDoesNotExist as e:
            form = AboutMeForm(request.POST, request.FILES)
            print(e)

        if form.is_valid():
            about_me = form.save(commit=False)
            user = request.user
            about_me.user = user
            about_me.save()

            return redirect("portfolio:index")

    return render(request, "edit_about.html", {"form": form})


def delete_about(request):
    """Delete 'about' of current user."""
    try:
        about_me = AboutMe.objects.get(user=request.user)
        about_me.delete()
    except ObjectDoesNotExist as e:
        print(e)

    return redirect("portfolio:index")


def edit_experience(request, id=None):
    """Edit experience page view."""
    if request.method == "GET":
        data_experience = None
        if id is not None:
            data_experience = get_object_or_404(Experience, pk=id)
            form = ExperienceForm(instance=data_experience)
        else:
            form = ExperienceForm()

    if request.method == "POST":
        if id is not None:
            data_experience = get_object_or_404(Experience, pk=id)
            form = ExperienceForm(request.POST, request.FILES, instance=data_experience)
        else:
            form = ExperienceForm(request.POST, request.FILES)

        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return redirect("portfolio:index")

    context = {
        'form': form,
        'data_experience': data_experience
    }
    return render(request, "edit_experience.html", context)


def delete_experience(request, id):
    """Delete 'Experience' of current user by id."""
    experience = get_object_or_404(Experience, pk=id)
    experience.delete()

    return redirect("portfolio:index")