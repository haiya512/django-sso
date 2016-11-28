from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^$', 'provider.views.index'),
                       url(r'^$', 'provider.views.new_index'),
                       url(r'^login$', 'provider.views.login', name='loginurl'),
                       url(r'^logout$', 'provider.views.logout'),
                       url(r'^register', 'provider.views.register'),
                       )
