from django.conf.urls import url,patterns

urlpatterns = patterns('',
	url(r'^', 'app.views.index', name='index'),


)