from django.urls import path
from . import views
from django.conf.urls import url
from  . import views as core_views
from .views import dashboard
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.index, name='home'),
    path('<str:req_id>/<str:email_id><int:level>/', views.feedback, name='feedback'),
    path("search_candidate/", views.search_candidate, name = 'search_candidate'),
    path('test/', views.test, name = 'test_name'),
     path('signup/', views.signup_view, name='signup'),
      path('login/', views.login_view, name='login'),
       url(r"^dashboard/", dashboard, name="dashboard"),
       
      path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),

        path('activate/<uidb64>/<token>/',views.activate, name='activate'), 

]
