from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'catansolver.views.home', name='home'),
)
