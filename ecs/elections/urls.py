from django.conf.urls import url

from ecs.elections.views import *

urlpatterns = [
    url(r'^list/$', ElectionListView.as_view(), name='election_list'),
    url(r'^new/$', ElectionCreateView.as_view(), name='election_create'),
    url(r'^delete/(?P<pk>\d+)/$', ElectionDeleteView.as_view(), name='election_delete'),
    url(r'^details/(?P<pk>\d+)/$', ElectionDetailView.as_view(), name='election_details'),
]
