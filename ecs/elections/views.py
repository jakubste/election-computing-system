from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from ecs.elections.forms import ElectionForm
from ecs.elections.models import Election
from ecs.utils.views import LoginRequiredMixin


class ElectionListView(LoginRequiredMixin, ListView):
    model = Election
    template_name = 'election_list.html'
    context_object_name = 'elections'

    def get_queryset(self):
        qs = super(ElectionListView, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class ElectionCreateView(LoginRequiredMixin, CreateView):
    form_class = ElectionForm
    template_name = 'election_create.html'
    success_url = reverse_lazy('elections:election_list')

    def get_form_kwargs(self):
        kwargs = super(ElectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ElectionDeleteView(DeleteView):
    model = Election
    template_name = 'election_delete.html'

    def get_success_url(self):
        return reverse('elections:election_list')


class ElectionDetailView(DetailView):
    model = Election
    template_name = 'election_details.html'
    context_object_name = 'election'
