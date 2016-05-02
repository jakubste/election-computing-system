from django.conf.urls import url

from ecs.elections.views import *

urlpatterns = [
    url(r'^list/$', ElectionListView.as_view(), name='election_list'),
    url(r'^new/$', ElectionCreateView.as_view(), name='election_create'),
]
