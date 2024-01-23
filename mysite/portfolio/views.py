from django.shortcuts import render, redirect
from .forms import AboutMeForm
from .models import AboutMe
from django.core.exceptions import ObjectDoesNotExist
# from django.http import HttpResponse


def index(request):
    """Index of portfolio app."""
    data = None
    if request.method == "GET":
        user = request.user
        data = AboutMe.objects.filter(user=user).first()

    return render(request, "index.html", {"data_": data})


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

            return redirect("index")

    return render(request, "edit.html", {"form": form})


def delete_about(request):
    """Delete 'about' of current user."""
    try:
        about_me = AboutMe.objects.get(user=request.user)
        about_me.delete()
    except ObjectDoesNotExist as e:
        print(e)

    return redirect("index")