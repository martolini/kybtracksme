from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('kybsal.slave.views',
    # Examples:
    # url(r'^$', 'kybsal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', 'login_view', name='login'),
    url(r'^signup/$', 'signup_view', name='signup'),
    url(r'^logout/$', 'logout_view', name='logout'),
)
