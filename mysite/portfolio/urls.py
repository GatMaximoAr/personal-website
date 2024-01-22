from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/", views.edit_about, name="edit")
]