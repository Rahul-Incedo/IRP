from django.urls import path
from . import views
from django.conf.urls import url
from  . import views as core_views

from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.signup_view, name = 'first_page'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name = 'signup'),
    path('logout/', views.logout_view, name = 'logout_page'),
    #    url(r"^dashboard/", dashboard, name="dashboard"),

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
