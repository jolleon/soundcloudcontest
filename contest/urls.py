from django.conf.urls import patterns, url

from contest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'contest/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^(?P<contest_id>\d+)/$', views.contest, name='contest')
)

