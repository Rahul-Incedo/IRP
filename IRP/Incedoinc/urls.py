from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("candidate/create", views.create_candidate_view, name="create_candidate_page")
]
