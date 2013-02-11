from django.conf.urls import patterns, url

from contest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)

