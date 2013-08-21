from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^tenk/', include('tenk_dashboard.urls')),
    url(r'^tenk/admin/', include(admin.site.urls)),
)
