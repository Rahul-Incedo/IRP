from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path('<str:req_id>/<str:email_id><int:level>/', views.feedback, name='feedback'),
    path("search_candidate/", views.search_candidate, name = 'search_candidate'),
    path('test/', views.test, name = 'test_name'),
]
