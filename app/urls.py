from django.conf.urls import url,patterns
from django.views.decorators.csrf import csrf_exempt
from app import views
urlpatterns = patterns('',

    url(r'^$',csrf_exempt(views.UploadFileView.as_view()),name='fileupload'),
    url(r'^report', views.ReportView.as_view(), name='report')

)