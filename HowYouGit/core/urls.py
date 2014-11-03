from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'HowYouGit.core.views.index'),
    url(r'^location/$', 'HowYouGit.core.views.location'),
    url(r'^repos_location/$', 'HowYouGit.core.views.repos_location'),
)
