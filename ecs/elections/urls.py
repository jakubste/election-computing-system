from django.conf.urls import url

from ecs.elections.views import *

urlpatterns = [
    url(r'^list/$', ElectionListView.as_view(), name='election_list'),
    url(r'^new/$', ElectionCreateView.as_view(), name='election_create'),
    url(r'^delete/(?P<pk>\d+)/$', ElectionDeleteView.as_view(), name='election_delete'),
    url(r'^details/(?P<pk>\d+)/$', ElectionDetailView.as_view(), name='election_details'),
    url(r'^load_data/(?P<pk>\d+)/$', ElectionLoadDataFormView.as_view(), name='election_load_data'),
    url(r'^generate_data/(?P<pk>\d+)/$', ElectionGenerateDataFormView.as_view(), name='election_generate'),
    url(r'^paint/(?P<pk>\d+)/$', ElectionPaintDataFormView.as_view(), name='election_paint'),
    url(r'^chart_data/(?P<pk>\d+)/$', ElectionChartView.as_view(), name='chart_data'),
    url(r'^add_result/(?P<pk>\d+)/$', ResultCreateView.as_view(), name='result_create'),
    url(r'^result/(?P<pk>\d+)/$', ResultDetailsView.as_view(), name='result_details'),
    url(r'^result/(?P<pk>\d+)/delete/$', ResultDeleteView.as_view(), name='result_delete'),
    url(r'^chart_data/result/(?P<pk>\d+)/$', ResultChartView.as_view(), name='result_chart_data'),
    url(r'^algorithms_chart_data/(?P<pk>\d+)/$', AlgorithmsChartView.as_view(), name='algorithms_chart_data'),
]
