from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'catansolver.views.home', name='home'),
    url(r'^board.json$', 'catansolver.views.new_board', name='board'),
)
