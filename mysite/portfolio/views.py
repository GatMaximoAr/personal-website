from django.shortcuts import render, redirect
from .forms import AboutMeForm
from .models import AboutMe
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
    if request.method == "POST":
        form = AboutMeForm(request.POST, request.FILES)

        if form.is_valid():
            about_me = form.save(commit=False)
            user = request.user
            about_me.user = user
            about_me.save()

            return redirect("index")
    else:
        form = AboutMeForm()

    return render(request, "edit.html", {"form": form})