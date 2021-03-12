from django.urls import path, re_path
from . import views
from django.conf.urls import url
from .views import dashboard, manage_jd_view, manage_job_view, upload_jd_view, upload_job_view, view_jd_view, view_job_view
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    # path("", views.index, name='home'),
    path("home/",views.home_view, name='home_page'),
    path("manage-jd/upload/", views.upload_jd_view, name='upload_jd_page'),
    path("manage-job/upload/", views.upload_job_view, name='upload_job_page'),
    path('manage-jd/', views.manage_jd_view, name='manage_jd_page'),
    path('manage-job/', views.manage_job_view, name='manage_job_page'),
    path("add-candidate/", views.add_candidate_view, name='add_candidate_page'),

    # view objects
    url(r'^files(?P<file_url>.*)/$', views.file_view, name='file_view'),

    url(r'^jd/(?P<jd_pk>.*)/view/$', views.view_jd_view, name='view_jd'),
    url(r'^job/(?P<job_pk>.*)/view/$', views.view_job_view, name='view_job'),

    # edit objects
    url(r'^job/(?P<job_pk>.*)/edit/$', views.edit_job_view, name='edit_job'),


    # delete objects
    url(r'^jd/(?P<jd_pk>.*)/delete/$', views.delete_jd_view, name='delete_jd'),
    url(r'^job/(?P<job_pk>.*)/delete/$', views.delete_job_view, name='delete_job'),

    # manage candidates and feedback
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/', views.feedback, name='feedback'),
    path("search_candidate/", views.search_candidate, name = 'search_candidate'),
    path('test/', views.test, name = 'test_name'),
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/edit<str:feedback_id>/', views.edit, name ='edit'),
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/field/<str:feedback_id>/', views.field_view, name = 'field'),
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/<str:field_name><int:del_level>/', views.delete_field, name = 'delete_field'),
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/Download/', views.download_report, name = "download_report"),

    path('delete_temp/', views.delete_temp, name = 'delete_temp'),
    path('delete_resume/media/Resume/<str:resume_name>', views.delete_resume, name="delete_temp_resume"),
    path("search_candidate/<str:candidate_email>", views.search_candidate, name = 'search_candidate_email'),
    path("edit_candidate/<str:candidate_email>/", views.edit_candidate, name = 'edit_candidate'),
    path("view_candidate/<str:candidate_email>/", views.view_candidate, name = 'view_candidate'),
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/report/', views.report_view, name = "report_view"),

    path('referrals/', views.referrals_view, name = "referrals_page"),
    path('referrals/refer_candidate/<str:requisition_id>/', views.refer_candidate_view, name = "refer_candidate_page"),
    path('referrals/my_referrals/<str:employee_id>/', views.my_referrals_view, name = "my_referrals_page"),

    # auditlog
    path('auditlog/', views.audit_log_view, name="auditlog"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
