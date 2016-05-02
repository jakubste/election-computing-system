from django.conf.urls import url

from ecs.accounts.views import *

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
]
