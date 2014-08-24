from django.conf.urls import url,patterns
from django.views.decorators.csrf import csrf_exempt
from app import views
urlpatterns = patterns('',

    url(r'^$',csrf_exempt(views.UploadFileView.as_view()),name="fileupload"),
    url(r'^report/(?P<report_id>[0-9]+)/(?P<file_1_id>[0-9]+)/(?P<file_2_id>[0-9]+)/$', views.ReportView.as_view(), name="report"),
    url(r'^report/(?P<report_id>[0-9]+)/$', views.ReportFileListView.as_view(), name="report_file_list")
)