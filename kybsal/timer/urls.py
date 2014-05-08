from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('kybsal.timer.views',
    # Examples:
    # url(r'^$', 'kybsal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^sjekk_in/$', 'timer_sjekk_in', name='sjekk_in'),
    url(r'^pause/$', 'timer_pause', name='pause'),
    url(r'^sjekk_ut/$', 'timer_sjekk_ut', name='sjekk_ut'),
    url(r'^pauserom/$', 'pause_rom', name='pause_rom'),
    url(r'^toppliste/$', 'toppliste', name='toppliste'),
)
