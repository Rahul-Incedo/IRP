from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("candidate/add", views.add_candidate_view, name="add_candidate_page"),
]
