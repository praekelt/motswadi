from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'motswadi.views.home', name='home'),
    # url(r'^motswadi/', include('motswadi.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
