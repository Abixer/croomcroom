from django.conf.urls import patterns, url

from preview import views

urlpatterns = patterns('',
	url(r'^$', views.preview, name='preview'),

)