import json

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.forms.widgets import Select
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, FormView

from ecs.elections.algorithms.brute_force import BruteForce
from ecs.elections.algorithms.genetic import GeneticAlgorithm
from ecs.elections.algorithms.greedy_algorithm import GreedyAlgorithm
from ecs.elections.algorithms.greedy_cc import GreedyCC
from ecs.elections.election_generator import ElectionGenerator
from ecs.elections.election_paint_loader import ElectionPaintLoader
from ecs.elections.exceptions import CandidatesNameIncorrectFormatException, SummingLineTypeException, \
    BadDataFormatException, PreferenceOrderTypeException, PreferenceOrderLogicException
from ecs.elections.exceptions import IncorrectTypeOfCandidatesNumberException, SummingLineFormatException
from ecs.elections.forms import ElectionForm, ElectionLoadDataForm, ElectionGenerateDataForm, ResultForm, \
    GeneticAlgorithmForm
from ecs.elections.helpers import check_votes_number_unique_votes_relation, check_vote_consistency, \
    check_number_of_votes_consistency
from ecs.elections.models import Election, Candidate, Voter, BRUTE_ALGORITHM, Result, GENETIC_ALGORITHM
from ecs.elections.models import GREEDY_ALGORITHM, GREEDY_CC
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
        if self.object.voters.count() <= 100:
            ctx['voters'] = self.object.voters.all().prefetch_related('preferences', 'preferences__candidate')
        ctx['results'] = self.object.results.all() \
            .select_related('geneticalgorithmsettings').prefetch_related('winners')
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


class ElectionPaintView(ConfigureElectionMixin, TemplateView):
    template_name = 'election_paint_data.html'
    election = None

    def dispatch(self, request, *args, **kwargs):
        self.election = get_object_or_404(Election, pk=kwargs.get('pk'))
        if self.election.user != self.request.user:
            raise Http404
        return super(ElectionPaintView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ElectionPaintView, self).get_context_data(**kwargs)
        ctx['election'] = self.election
        return ctx

    def post(self, request, pk):
        data = json.loads(request.body)
        loader = ElectionPaintLoader(self.election, data['candidates'], data['voters'])
        loader.load_elections()
        return HttpResponse(reverse("elections:election_details", args=(self.election.pk,)))


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

    def get_title(self):
        return 'Voters and candidates distribution'

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
            GREEDY_ALGORITHM: GreedyAlgorithm,
            GREEDY_CC: GreedyCC,
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
    algorithm_keys = {
        'b': 'Brute Force',
        'g': 'Genetic',
        'r': 'Greedy',
        'c': 'Greedy CC'
    }

    def dispatch(self, request, *args, **kwargs):
        try:
            self.result = Result.objects.get(pk=kwargs['pk'])
            self.election = self.result.election
        except Result.DoesNotExist:
            raise Http404
        return super(ResultChartView, self).dispatch(request, *args, **kwargs)

    def get_title(self):
        return 'Result for algorithm: %s with p: %d' % (
            self.algorithm_keys[self.result.algorithm], self.result.p_parameter)

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
    points_stroke_colors = ['red', 'green', 'gold', 'silver']
    algorithm_keys = ['b', 'g', 'r', 'c']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.results = Result.objects.filter(winners__result__election=kwargs['pk']).distinct()
        except Result.DoesNotExist:
            raise Http404
        return super(AlgorithmsChartView, self).dispatch(request, *args, **kwargs)

    def get_data(self):
        """
        :return: algorithms' datasets - dictionary with five keys
            'b' - for brute\n
            'g' - for genetic\n
            'r' - for greedy\n
            'c' - for greedy_cc\n
                'b', 'g', 'r', 'c' - stores times measured for given entry on x_axis list
            Under 'i' index only one and at least one of the four above lists can store
            a time - other three lists have to store None value under 'i'-th index
                'x_axis' - label for x axis - stores list of p_parameter values
            Each of five lists contains the list of the same length
        """
        # TODO use constants from models.py after greedy branch merge
        times_and_labels = {'b': [], 'g': [], 'r': [], 'c': [], 'x_axis': []}

        prev_p = 0
        max_list_length = 0

        for result in self.results:
            if prev_p != result.p_parameter:
                self.fill_up_with_nones(self.algorithm_keys, max_list_length, prev_p, times_and_labels)
                prev_p = result.p_parameter
            times_and_labels[result.algorithm].append(result.time)
            list_length = len(times_and_labels[result.algorithm])
            max_list_length = list_length if list_length > max_list_length else max_list_length

        self.fill_up_with_nones(self.algorithm_keys, max_list_length, prev_p, times_and_labels)

        return times_and_labels

    @staticmethod
    def fill_up_with_nones(algorithm_keys, max_list_length, prev_p, times_and_labels):
        while len(times_and_labels['x_axis']) < max_list_length:
            times_and_labels['x_axis'].append(prev_p)
        for key in algorithm_keys:
            while len(times_and_labels[key]) < max_list_length:
                times_and_labels[key].append(None)

    def get_datasets(self, *args, **kwargs):
        """
        Format data to Scatter dataset format
        """
        algorithm_keys = ['b', 'g', 'r', 'c']
        labels = self.get_labels()
        colors = self.get_colors()
        point_stroke_colors = self.get_points_stroke_colors()
        points_radii = self.get_points_radii()
        data = self.get_data()

        datasets = [
            {
                'fill': False,
                'label': labels[i],
                'borderColor': colors[i],
                'backgroundColor': point_stroke_colors[i],
                'data': data[algorithm_keys[i]],
                'pointRadius': points_radii[i],
                'cubicInterpolationMode': 'monotone'
            }
            for i in xrange(self.datasets_number)
            ]

        return {
            'labels': data['x_axis'],
            'datasets': datasets
        }
