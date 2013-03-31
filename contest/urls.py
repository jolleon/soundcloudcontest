from django.conf.urls import patterns, url

from contest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^contests$', views.contests, name='contests'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'contest/login.html'}, name="login"),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^soundcloud_signin/$', views.soundcloud_signin, name='soundcloud_signin'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^(?P<contest_id>\d+)/$', views.contest, name='contest'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit/(?P<contest_id>\d+)/$', views.edit, name='edit'),
)

