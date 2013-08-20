from django.conf.urls import patterns, url

from tenk_dashboard import views
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<participant_id>\d+)/$', views.update, name='update'),
)