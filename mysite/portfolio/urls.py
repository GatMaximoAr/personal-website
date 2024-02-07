from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path("", views.index, name="index"),
    path("add/about/", views.AddAboutMe.as_view(), name="add_about"),
    path("edit/about/<int:pk>", views.EditAboutMe.as_view(), name="edit_about"),
    path("delete/about/", views.delete_about, name="delete_about"),
    path("add/experience/", views.AddExperience.as_view(), name="add_experience"),
    path("edit/experience/<int:pk>", views.EditExperience.as_view(), name="edit_experience"),
    path("delete/experience/<int:id>", views.delete_experience, name="delete_experience")
]