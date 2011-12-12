from django.conf.urls.defaults import patterns, include, url
from ebooks import views
from settings import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.overview),
    url(r'show/(?P<type>\w+)/(?P<dataid>\d+)/', views.show_data ),
    url(r'manage/ebooks/', views.manage_ebooks ),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve'),

    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)