from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/about/", views.edit_about, name="edit_about"),
    path("delete/about/", views.delete_about),
    path("edit/experience/", views.edit_experience, name="edit_experience"),
    path("edit/experience/<int:id>", views.edit_experience, name="edit_experience"),
    path("delete/experience/<int:id>", views.delete_experience, name="delete_experience")
]