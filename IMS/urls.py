from django.conf.urls import patterns, include, url
from django.conf import settings 
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IMS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^demo/', include('demo.urls')),
	url(r'^demo/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
	#url(r'', include('preview.urls')),
	url(r'', include('demo.urls')),
	url(r'^demo/', include('allauth.urls')),
)

#Serving user uploaded files in a pretty shitty way.
if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name="media"),
	)
