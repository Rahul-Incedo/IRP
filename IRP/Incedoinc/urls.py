from django.urls import path
from Incedoinc import views

urlpatterns = [
    path("", views.index),
    path("candidate/create", views.create_candidate_view, name="create_candidate_page"),
    path("home/",views.home),
]
