from django.urls import path
from . import views
from django.conf.urls import url
from  . import views as core_views
from .views import dashboard, manage_jd_view, manage_job_view, upload_jd_view, upload_job_view
from django.contrib.auth import views as auth_views

#download-file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #pulkit-kartikeyan
    path("", views.index, name='home'),
    path("home/",views.home_view, name='home_page'),
    path("upload-jd/", views.upload_jd_view, name='upload_jd_page'),
    path("upload-job/", views.upload_job_view, name='upload_job_page'),
    path('manage-jd/', views.manage_jd_view, name='manage_jd_page'),
    path('manage-job/', views.manage_job_view, name='manage_job_page'),
    # path("search-jd/<str:requisition_id>/", views.search_jd_view, name='search_jd_page'),
    # path('media/<str:path>/', views.download_view),
    path("add-candidate/", views.add_candidate_view, name='add_candidate_page'),

    #vaishnavi
    path('signup_/', views.signup_view, name='signup_'),
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
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/edit<int:edit_level>/', views.edit, name ='edit'),
    path("search_candidate/<str:candidate_email>", views.search_candidate, name = 'search_candidate_email'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)