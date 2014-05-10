from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kybsal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^', 'kybsal.timer.views.vedlikehold'),
    url(r'^$', 'kybsal.timer.views.frontpage', name='frontpage'),
    url(r'^search/$', 'kybsal.slave.views.search_view', name='search'),
    url(r'^slave/', include('kybsal.slave.urls')),
    url(r'^timer/', include('kybsal.timer.urls')),
    url(r'^kontakt/', 'kybsal.contact.views.contact', name='kontakt'),
    url(r'^spritz/', include('kybsal.spritz.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
