from django.conf.urls import url,patterns
from app import views
urlpatterns = patterns('',

    url(r'^',views.UploadFileView.as_view(),name='fileupload'),

)