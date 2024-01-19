from django.shortcuts import render
from .forms import AboutMeForm
# from django.http import HttpResponse


def index(request):
    """Index of portfolio app."""
    if request.method == "POST":
        form = AboutMeForm(request.POST, request.FILES)

        if form.is_valid():
            about_me = form.save(commit=False)
            user = request.user
            about_me.user = user
            about_me.save()

            return render(request, "index.html", {"data_": about_me})
    else:
        form = AboutMeForm()

    return render(request, "index.html", {"form": form})