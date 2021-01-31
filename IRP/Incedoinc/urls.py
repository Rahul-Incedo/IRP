from django.urls import path
from . import views

urlpatterns = [
    #working
    path("", views.index),
    path("home/",views.home_view, name='home_page'),
    path("upload-jd/", views.upload_jd_view, name='upload_jd_page'),
    path("add-candidate", views.add_candidate_view, name='add_candidate_page'),
    #to be developed
    path("search-jd/<str:requisition_id>/", views.search_jd_view, name='search_jd_page'),
    path("search-candidate/", views.search_candidate_view, name='search_candidate_page'),
    path('feedback/<str:req_id>/<str:email_id><int:level>/', views.feedback, name='feedback'),
    
    path('test', views.test_view, name='test_page')
]
