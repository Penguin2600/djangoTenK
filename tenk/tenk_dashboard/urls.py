from django.conf.urls import patterns, url

from tenk_dashboard import views
urlpatterns = patterns('',
    url(r'^auth/$', 'django.contrib.auth.views.login', {'template_name': 'tenk_dashboard/auth.html'}, name='login'),
    url(r'^auth/logout/$', views.logout_view, name='logout'),

    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^$', views.CreateView.as_view(), name='index'),
    url(r'^quick/$', views.QuickView.as_view(), name='quick'),


    url(r'^update/(?P<participant_id>\d+)/$', views.UpdateView.as_view(), name='update'),
    url(r'^update/$', views.UpdateView.as_view(), name='update'),

    url(r'^import/$', views.ImportView.as_view(), name='csv_import'),
    url(r'^export/$', views.ExportView.as_view(), name='csv_export'),

    url(r'^stats/$', views.StatsView.as_view(), name='stats'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^checkbib/(?P<bib_number>\d+)/$', views.checkbib_view, name='checkbib'),
    url(r'^checksearch/(?P<query>\w+)/$', views.checksearch_view, name='checksearch'),

)