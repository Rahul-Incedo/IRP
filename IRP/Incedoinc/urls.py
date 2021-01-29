from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("candidate/add", views.add_candidate_view, name="add_candidate_page"),
    path("user/upload_jd", views.upload_jd_view, name="upload_jd_page"),
    path("home/",views.home),
    path("search_jd/<str:requisition_id>/", views.search_jd_view),
    path('<str:req_id>/<str:email_id><int:level>/', views.feedback, name='feedback'),
    path("search_candidate/", views.search_candidate, name = 'search_candidate'),
    path('test/', views.feedback, name = 'test_name'),

]
