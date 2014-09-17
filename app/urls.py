from django.conf.urls import url,patterns
from django.views.decorators.csrf import csrf_exempt
from app import views
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = patterns('',

    url(r'^$', RedirectView.as_view(url=reverse_lazy("report_list")) , name="index"),
    url(r'^about$', views.AboutView.as_view(), name="about"),
    url(r'^upload/$$', csrf_exempt(views.UploadFileView.as_view()) , name="fileupload"),
    url(r'^report/(?P<report_id>[0-9]+)/(?P<file_1_id>[0-9]+)/(?P<file_2_id>[0-9]+)/$', views.ComparisonView.as_view(), name="report"),
    url(r'^report/(?P<report_id>[0-9]+)/$', views.ReportView.as_view(), name="report_file_list"),
    url(r'^report/list/$', views.ReportListView.as_view(), name="report_list")
)