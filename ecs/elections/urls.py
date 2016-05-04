from django.conf.urls import url

from ecs.elections.views import *

urlpatterns = [
    url(r'^list/$', ElectionListView.as_view(), name='election_list'),
    url(r'^new/$', ElectionCreateView.as_view(), name='election_create'),
    url(r'^delete/(?P<pk>\d+)/$', ElectionDeleteView.as_view(), name='election_delete'),
    url(r'^details/(?P<pk>\d+)/$', ElectionDetailView.as_view(), name='election_details'),
    url(r'^load_data/(?P<pk>\d+)/$', ElectionLoadDataFormView.as_view(), name='election_load_data'),
    url(r'^generate_data/(?P<pk>\d+)/$', ElectionGenerateDataFormView.as_view(), name='election_generate'),
    url(r'^details/(?P<pk>\d+)/chart/$', ScatterChartJSONView.as_view(), name='chart_data'),
]
