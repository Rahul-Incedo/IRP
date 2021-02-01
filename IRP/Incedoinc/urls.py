from django.urls import path
from . import views
from django.conf.urls import url
from  . import views as core_views
from .views import dashboard
from django.contrib.auth import views as auth_views


urlpatterns = [
    #pulkit-kartikeyan
    path("", views.index, name='home'),
    path("home/",views.home_view, name='home_page'),
    path("upload-jd/", views.upload_jd_view, name='upload_jd_page'),
    path("add-candidate/", views.add_candidate_view, name='add_candidate_page'),
    path("search-jd/<str:requisition_id>/", views.search_jd_view, name='search_jd_page'),

    #vaishnavi
    path('signup/', views.signup_view, name='signup'),
    path('login_/', views.login_view, name='login_'),
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

    ## rudra
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/', views.feedback, name='feedback'),
    path("search_candidate/", views.search_candidate, name = 'search_candidate'),
    path('test/', views.test, name = 'test_name'),

]
