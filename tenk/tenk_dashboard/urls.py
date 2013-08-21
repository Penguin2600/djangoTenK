from django.conf.urls import patterns, url

from tenk_dashboard import views
urlpatterns = patterns('',
    url(r'^auth/$', 'django.contrib.auth.views.login', {'template_name': 'tenk_dashboard/auth.html'}, name='login'),
    url(r'^auth/logout/$', views.logout_view, name='logout'),
    url(r'^create/$', views.create_view, name='create'),
    url(r'^$', views.create_view, name='index'),
    url(r'^(?P<participant_id>\d+)/$', views.update_view, name='update'),
    url(r'^stats/$', views.stats_view, name='stats'),
    url(r'^import/$', views.import_view, name='csv_import'),
    url(r'^checkbib/(?P<bib_number>\d+)/$', views.checkbib_view, name='checkbib'),
)