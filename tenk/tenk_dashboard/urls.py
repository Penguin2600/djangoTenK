from django.conf.urls import patterns, url

from tenk_dashboard import views
urlpatterns = patterns('',
    url(r'^auth/$', 'django.contrib.auth.views.login', {'template_name': 'tenk_dashboard/auth.html'}, name='login'),
    url(r'^auth/logout/$', views.logout_view, name='logout'),

    url(r'^create/$', views.create_view, name='create'),
    url(r'^quick/$', views.quick_create_view, name='quick'),
    url(r'^$', views.create_view, name='index'),

    url(r'^update/(?P<participant_id>\d+)/$', views.update_view, name='update'),
    url(r'^update/$', views.update_view, name='update'),

    url(r'^import/$', views.csv_import_view, name='csv_import'),
    url(r'^export/$', views.csv_export_view, name='csv_export'),

    url(r'^stats/$', views.stats_view, name='stats'),
    url(r'^search/$', views.search_view, name='search'),
    url(r'^checkbib/(?P<bib_number>\d+)/$', views.checkbib_view, name='checkbib'),
)