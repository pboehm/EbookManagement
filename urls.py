from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ebooks import views
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.overview),
    url(r'show/(?P<type>\w+)/(?P<dataid>\d+)/', views.show_data ),

    url(r'studip', views.studip_json_data),

    url(r'manage/ebooks/$', views.manage_ebooks ),
    url(r'manage/ebooks/move/$', views.submit_ebook_move ),
    url(r'manage/ebooks/add/$', views.add_ebook),

    url(r'search/$', views.search_items),

    url(r'manage/user/profile/$', views.manage_user_profile),
    url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'} ),
    url(r'logout/$', 'django.contrib.auth.views.logout_then_login' ),

    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

