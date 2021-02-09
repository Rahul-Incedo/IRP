from django.urls import path
from . import views
from django.conf.urls import url
from  . import views as core_views

from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.login_view, name = 'first_page'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name = 'signup'),
    path('logout/', views.logout_view, name = 'logout'),
    #    url(r"^dashboard/", dashboard, name="dashboard"),

 #youtube.com/watch?v=sFPcd6myZrY&t=728s

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

    path('activate/<uidb64>/<token>/',views.activate, name='activate'),  # name = 'activate'
    
    
    #  path('change_password/', auth_views.PasswordChangeView.as_view(template_name = 'accounts/change_password_page.html'), name = 'change_password_page'),
     path('change_password/', views.change_password_view.as_view(template_name = 'accounts/change_password_page.html'), name = 'change_password_page'), #6.36
     path('password_success/',views.password_success, name = 'password_success')
]
