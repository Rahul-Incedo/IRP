from django.urls import path
from . import views
from django.conf.urls import url
from  . import views as core_views

from django.contrib.auth import views as auth_views


urlpatterns = [
    #pulkit-kartikeyan
    #path("", views.index, name='home'),
    path("home/",views.home_view, name='home_page'),
    path("upload-jd/", views.upload_jd_view, name='upload_jd_page'),
    path("add-candidate/", views.add_candidate_view, name='add_candidate_page'),
    path("search-jd/<str:requisition_id>/", views.search_jd_view, name='search_jd_page'),

    #vaishnavi
    

    ## rudra
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/', views.feedback, name='feedback'),
    path("search_candidate/", views.search_candidate, name = 'search_candidate'),
    path('test/', views.test, name = 'test_name'),

]
