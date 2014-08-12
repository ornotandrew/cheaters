from django.conf.urls import url,patterns
from app import views
urlpatterns = patterns('',

    url(r'^$',views.UploadFileView.as_view(),name='fileupload'),
    url(r'^report', views.ReportView.as_view(), name='report')

)