from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("candidate/add", views.add_candidate_view, name="add_candidate_page"),
    path("user/upload_jd", views.upload_jd_view, name="upload_jd_page"),
    path("home/",views.home),
    path("search_jd/<str:requisition_id>/", views.search_jd_view)
]
