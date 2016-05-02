from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from ecs.elections.forms import ElectionForm
from ecs.elections.models import Election


class ElectionListView(ListView, LoginRequiredMixin):
    model = Election
    template_name = 'election_list.html'
    context_object_name = 'elections'

    def get_queryset(self):
        qs = super(ElectionListView, self).get_queryset()
        qs.filter(user=self.request.user)
        return qs


class ElectionCreateView(CreateView, LoginRequiredMixin):
    form_class = ElectionForm
    template_name = 'election_create.html'
    success_url = reverse_lazy('elections:election_list')

    def get_form_kwargs(self):
        kwargs = super(ElectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
