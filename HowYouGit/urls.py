from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from HowYouGit import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('HowYouGit.core.urls')),
    url(r'^admin/', include(admin.site.urls)),
) 