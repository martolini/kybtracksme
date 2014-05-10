from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('kybsal.spritz.views',
	url(r'^read/$', 'read_view', name='read'),
)
