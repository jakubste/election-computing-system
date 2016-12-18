from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.forms.fields import ChoiceField
from django.forms.widgets import ChoiceInput, Select
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, FormView

from ecs.elections.algorithms.brute_force import BruteForce
from ecs.elections.algorithms.genetic import GeneticAlgorithm
from ecs.elections.election_generator import ElectionGenerator
from ecs.elections.exceptions import CandidatesNameIncorrectFormatException, SummingLineTypeException, \
    BadDataFormatException, PreferenceOrderTypeException, PreferenceOrderLogicException
from ecs.elections.exceptions import IncorrectTypeOfCandidatesNumberException, SummingLineFormatException
from ecs.elections.forms import ElectionForm, ElectionLoadDataForm, ElectionGenerateDataForm, ResultForm, \
    GeneticAlgorithmForm
from ecs.elections.helpers import check_votes_number_unique_votes_relation, check_vote_consistency, \
    check_number_of_votes_consistency
from ecs.elections.models import Election, Candidate, Voter, BRUTE_ALGORITHM, Result, GENETIC_ALGORITHM
from ecs.geo.models import Point
from ecs.utils.chart_views import ChartMixin
from ecs.utils.views import LoginRequiredMixin


class ElectionListView(LoginRequiredMixin, ListView):
    model = Election
    template_name = 'election_list.html'
    context_object_name = 'elections'
    active_election_list = 'active'

    def get_queryset(self):
        qs = super(ElectionListView, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class ElectionCreateView(LoginRequiredMixin, CreateView):
    form_class = ElectionForm
    template_name = 'election_create.html'

    def get_form_kwargs(self):
        kwargs = super(ElectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        if self.object:
            return self.object.get_absolute_url()
        else:
            return reverse_lazy('elections:election_list')


class ConfigureElectionMixin(View):
    def dispatch(self, request, *args, **kwargs):
        self.election = get_object_or_404(Election, pk=kwargs.get('pk'))
        if self.election.user != self.request.user:
            raise Http404
        return super(ConfigureElectionMixin, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ConfigureElectionMixin, self).get_form_kwargs()
        kwargs['election'] = self.election
        return kwargs

    def get_success_url(self):
        return reverse('elections:election_details', args=(self.election.pk,))


class ElectionDeleteView(ConfigureElectionMixin, DeleteView):
    model = Election
    template_name = 'election_delete.html'

    def get_success_url(self):
        return reverse('elections:election_list')


class ElectionDetailView(DetailView):
    model = Election
    template_name = 'election_details.html'
    context_object_name = 'election'

    def get_context_data(self, **kwargs):
        ctx = super(ElectionDetailView, self).get_context_data(**kwargs)
        if self.object.voters.count() < 500:
            ctx['voters'] = self.object.voters.all().prefetch_related('preferences', 'preferences__candidate')
        ctx['results'] = self.object.results.all()
        choices = [(res.pk, str(res)) for res in ctx['results'].reverse()]
        choices.append((None, '------'))
        choices.reverse()
        ctx['results_choice'] = Select(choices=choices).render('results_choice', None)
        ctx['results_number'] = self.object.results.count()
        ctx['results_pks'] = ",".join([str(n) for n in self.object.results.values_list('pk', flat=True)])
        ctx['results_p_params'] = "," + ",".join(
            [str(n) for n in self.object.results.values_list('p_parameter', flat=True)]
        )
        ctx['results_descriptions'] = "No result," + ",".join(
            ['{}: p = {}'.format(r.get_algorithm_display(), r.p_parameter) for r in self.object.results.all()]
        )
        return ctx


class ElectionLoadDataFormView(ConfigureElectionMixin, FormView):
    form_class = ElectionLoadDataForm
    template_name = 'election_load_data.html'
    election = None

    def form_valid(self, form):
        file = form.cleaned_data['file']
        try:
            self.load_data_from_file(file)
        except Exception as exc:
            form.add_error('file', str(exc))
            return self.form_invalid(form)
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
                    raise CandidatesNameIncorrectFormatException(2 + i)
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
                    line = [int(x) for x in line]
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

            message = """
            <strong>Successfully added election data from file!</strong><br>
            * Candidates number: {}<br>
            * Voters number: {}<br>
            * Unique votes: {}<br>
            """
            messages.success(
                self.request,
                message.format(candidates_number, voters_number, unique_votes)
            )

        election_data.close()


class ElectionGenerateDataFormView(ConfigureElectionMixin, FormView):
    form_class = ElectionGenerateDataForm
    template_name = 'election_generate_data.html'
    election = None

    def form_valid(self, form):
        generator = ElectionGenerator(self.election, **form.cleaned_data)
        generator.generate_elections()
        return super(ElectionGenerateDataFormView, self).form_valid(form)


class ElectionChartView(ChartMixin):
    datasets_number = 2
    labels = ['Candidates', 'Voters']
    colors = ['black', 'black']
    points_stroke_colors = ['green', 'blue']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.election = Election.objects.get(pk=kwargs['pk'])
        except Election.DoesNotExist:
            raise Http404
        return super(ElectionChartView, self).dispatch(request, *args, **kwargs)

    def get_data(self):
        """
        Returns list of lists of points.
        First list for candidates, second for voters.
        """
        candidates = list(Point.objects.filter(candidate__election=self.election).values('x', 'y'))
        voters = list(Point.objects.filter(voter__election=self.election).values('x', 'y'))
        return [candidates, voters]


class ResultCreateView(ConfigureElectionMixin, CreateView):
    form_class = ResultForm
    template_name = 'result_create.html'

    def get_context_data(self, **kwargs):
        ctx = super(ResultCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            ctx['genetic_form'] = GeneticAlgorithmForm(self.request.POST)
        else:
            ctx['genetic_form'] = GeneticAlgorithmForm()
        return ctx

    def form_valid(self, form):
        result = super(ResultCreateView, self).form_valid(form)

        algorithm_kwargs = {}
        if form.cleaned_data['algorithm'] == GENETIC_ALGORITHM:
            genetic_form = GeneticAlgorithmForm(self.request.POST, result=self.object)
            if not genetic_form.is_valid():
                return self.form_invalid(form)
            algorithm_kwargs.update(genetic_form.cleaned_data)

        algorithm = {
            BRUTE_ALGORITHM: BruteForce,
            GENETIC_ALGORITHM: GeneticAlgorithm,
        }[form.cleaned_data['algorithm']]
        algorithm = algorithm(self.election, form.cleaned_data['p_parameter'], **algorithm_kwargs)
        time, winners = algorithm.start()
        self.object.time = time
        for winner in winners:
            self.object.winners.add(winner)
        self.object.score = self.object.calculate_score()
        self.object.save()

        if form.cleaned_data['algorithm'] == GENETIC_ALGORITHM:
            # noinspection PyUnboundLocalVariable
            genetic_form.save()

        return result


class ResultPermissionsMixin(View):
    def dispatch(self, request, *args, **kwargs):
        self.result = get_object_or_404(Result, pk=kwargs.get('pk'))
        if self.result.election.user != self.request.user:
            raise Http404
        return super(ResultPermissionsMixin, self).dispatch(request, *args, **kwargs)


class ResultDeleteView(DeleteView, ResultPermissionsMixin):
    model = Result
    template_name = 'result_delete.html'
    context_object_name = 'result'
    result_to_delete = None

    def get_success_url(self):
        return reverse('elections:election_details', args=(self.object.election_id,))


class ResultDetailsView(DetailView):
    model = Result
    template_name = 'result_details.html'
    context_object_name = 'result'


class ResultChartView(ChartMixin):
    datasets_number = 3
    labels = ['Voters', 'Candidates', 'Winners']
    colors = ['black', 'black', 'black']
    points_stroke_colors = ['blue', 'green', 'red']
    points_radii = [5, 5, 10]

    def dispatch(self, request, *args, **kwargs):
        try:
            self.result = Result.objects.get(pk=kwargs['pk'])
            self.election = self.result.election
        except Result.DoesNotExist:
            raise Http404
        return super(ResultChartView, self).dispatch(request, *args, **kwargs)

    def get_data(self):
        """
        Returns list of lists of points.
        First list for candidates, second for voters.
        """
        candidates = list(Point.objects.filter(candidate__election=self.election).values('x', 'y'))
        voters = list(Point.objects.filter(voter__election=self.election).values('x', 'y'))
        winners = list(
            Point.objects.filter(candidate__in=self.result.winners.all())
                .extra(select={'r': '2'}).values('x', 'y', 'r')
        )
        return [voters, candidates, winners]


class AlgorithmsChartView(ChartMixin):
    datasets_number = 4
    labels = ['Brute Force', 'Genetic', 'Greedy', 'Greedy CC']
    colors = ['red', 'green', 'gold', 'silver']
    points_stroke_colors = ['transparent', 'transparent', 'transparent', 'transparent']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.results = Result.objects.filter(winners__result__election=kwargs['pk']).distinct()
        except Result.DoesNotExist:
            raise Http404
        return super(AlgorithmsChartView, self).dispatch(request, *args, **kwargs)

    def get_data(self):
        """
        Time execution of given algorithms for given p parameter
        :return: algorithms' datasets
        """
        # TODO use constants from models.py after greedy branch merge
        brute = self.results_for_algorithm('b')
        genetic = self.results_for_algorithm('g')
        greedy = self.results_for_algorithm('r')
        greedy_cc = self.results_for_algorithm('c')
        return [brute, genetic, greedy, greedy_cc]

    def results_for_algorithm(self, algorithm_char_code):
        """
        :param algorithm_char_code: one of: 'r', 'g', 'b', 'c'
        :return: list of dicts { x: p_parameter, y: time } for algorithm specified by `algorithm_char_code`
        """
        results = list(self.results.filter(algorithm=algorithm_char_code))
        if not results:
            return []
        return [self.to_point(result.p_parameter, result.time) for result in results]

    @staticmethod
    def to_point(x, y):
        return {
            'x': x,
            'y': y
        }
    # def print_results(self, results):
    #     if not results:
    #         return
    #     for result in results:
    #         print ("p %d" % result['x'])
    #         print ("time %f" % result['y'])

