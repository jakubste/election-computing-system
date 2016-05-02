from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.http.response import Http404
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormView

from ecs.elections.exceptions import CandidatesNameIncorrectFormatException, SummingLineTypeException, \
    BadDataFormatException, PreferenceOrderTypeException, PreferenceOrderLogicException
from ecs.elections.exceptions import IncorrectTypeOfCandidatesNumberException, SummingLineFormatException
from ecs.elections.forms import ElectionForm, ElectionLoadDataForm
from ecs.elections.helpers import check_votes_number_unique_votes_relation, check_vote_consistency, \
    check_number_of_votes_consistency
from ecs.elections.models import Election, Candidate, Voter
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


class ElectionLoadDataFormView(FormView):
    form_class = ElectionLoadDataForm
    template_name = 'election_load_data.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.election = Election.objects.get(pk=kwargs['pk'])
        except:
            raise Http404
        if self.election.user != self.request.user:
            raise Http404
        return super(ElectionLoadDataFormView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ElectionLoadDataFormView, self).get_form_kwargs()
        kwargs['election'] = self.election
        return kwargs

    def get_success_url(self):
        return reverse('elections:election_details', args=(self.election.pk,))

    def form_valid(self, form):
        file = form.cleaned_data['file']
        self.load_data_from_file(file)
        return super(ElectionLoadDataFormView, self).form_valid(form)

    def load_data_from_file(self, election_data):
        with transaction.atomic():
            voters_number_in_loop = 0

            candidates_number = int(election_data.readline())
            if candidates_number <= 0:
                raise IncorrectTypeOfCandidatesNumberException

            # reading candidates' names
            for i in xrange(candidates_number):
                line = election_data.readline()
                try:
                    candidate_name = line.split(',', 1)[1].strip()
                    candidate_id = line.split(',', 1)[0].strip()
                except IndexError:
                    raise CandidatesNameIncorrectFormatException(2+i)
                Candidate.objects.create(
                    election=self.election,
                    name=candidate_name,
                    soc_id=candidate_id
                )

            # reading number of all votes and unique votes
            line = election_data.readline()
            line = line.split(',', 2)

            try:
                voters_number = int(line[1])
                unique_votes = int(line[2])
                check_votes_number_unique_votes_relation(voters_number, unique_votes)
            except IndexError:
                raise SummingLineFormatException(2 + candidates_number)
            except ValueError:
                raise SummingLineTypeException(2 + candidates_number)

            # reading order preferences
            for i in xrange(unique_votes):
                line = election_data.readline()
                if line == '':
                    raise BadDataFormatException
                line = line.split(',', candidates_number)
                try:
                    line = map(lambda x: int(x), line)
                except ValueError:
                    raise PreferenceOrderTypeException(3 + candidates_number + i)
                if line[0] <= 0 or line[0] > voters_number:
                    raise PreferenceOrderLogicException(3 + candidates_number + i)
                voters_number_in_loop += line[0]
                check_vote_consistency(line[1:], candidates_number)
                # vote = Vote(line[0], line[1:])
                voter = Voter.objects.create(
                    election=self.election,
                    repeats=line[0]
                )
                voter.set_preferences_by_ids(line[1:])

            check_number_of_votes_consistency(voters_number, voters_number_in_loop)

            # TODO: Message instead of print
            print '* Candidates number:', candidates_number
            print '* Voters number:', voters_number
            print '* Unique votes:', unique_votes

        election_data.close()
