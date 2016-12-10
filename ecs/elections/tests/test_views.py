import json
import os

import mock
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import RequestFactory

from ecs.elections.algorithms.brute_force import BruteForce
from ecs.elections.election_generator import ElectionGenerator
from ecs.elections.exceptions import *
from ecs.elections.factories import ElectionFactory, VoterFactory, PreferenceFactory, CandidateFactory, \
    PointCandidateFactory, PointVoterFactory, ResultFactory, UserFactory
from ecs.elections.models import Preference, BRUTE_ALGORITHM, Result
from ecs.elections.views import ElectionLoadDataFormView, ElectionChartView, ResultChartView
from ecs.utils.unittestcases import TestCase

mock.patch.object = mock.patch.object


class ElectionListTestCase(TestCase):
    def setUp(self):
        self.url = 'elections:election_list'

    def test_login_required(self):
        self.assertViewRequiresLogin()

    def test_list_own_elections(self):
        ElectionFactory.create()
        user = self.login()
        ElectionFactory.create(user=user)
        response = self.client.get(self.get_url())
        self.assertEqual(
            len(response.context['elections']),
            1
        )


class ElectionDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = self.login()
        self.election = ElectionFactory.create(user=self.user)

    def get_url(self):
        return reverse('elections:election_details', args=(self.election.pk,))

    def test_voters_in_context(self):
        v = VoterFactory(election=self.election)
        c = CandidateFactory(election=self.election)
        p = PreferenceFactory(voter=v, candidate=c)
        response = self.client.get(self.get_url())
        self.assertIn(
            'voters',
            response.context
        )
        self.assertIn(
            str(v.repeats),
            response.content
        )
        self.assertIn(
            p.candidate.name,
            response.content
        )


class ElectionLoadDataFromFileTestCase(TestCase):
    def setUp(self):
        self.user = self.login()
        self.election = ElectionFactory.create(user=self.user)
        self.url = reverse('elections:election_load_data', args=(self.election.pk,))

    def get_url(self):
        return self.url

    @mock.patch('ecs.elections.views.messages')
    def test_load_data_from_file(self, mocked_messages):
        # basic test for data loading
        filename = 'test_data1.txt'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        request = RequestFactory().get(self.get_url())
        view = ElectionLoadDataFormView(request=request, election=self.election)
        view.load_data_from_file(open(filename))
        self.assertListEqual(
            [c.name for c in self.election.candidates.all()],
            ['Monika', 'Weronika', 'Beata', 'Zuzanna', 'Alicja']
        )
        self.assertEqual(Preference.objects.count(), 20)
        mocked_messages.success.assert_called()

    def test_load_data_from_file_by_form(self):
        filename = 'test_data1.txt'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.get_url(), {
            'file': open(filename)
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.election.voters.count(), 4)
        self.assertEqual(self.election.candidates.count(), 5)
        self.assertEqual(Preference.objects.filter(candidate__election=self.election).count(), 20)

    def test_incorrect_type_of_candidates_number_exception(self):
        filename = 'test_exceptions1.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(IncorrectTypeOfCandidatesNumberException()), str(response.context['form'].errors))

    def test_candidates_name_incorrect_format_exception(self):
        filename = 'test_exceptions2.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(CandidatesNameIncorrectFormatException(2)), str(response.context['form'].errors))

    def test_summing_line_format_exception(self):
        filename = 'test_exceptions3.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(SummingLineFormatException(5)), str(response.context['form'].errors))

    def test_summing_line_type_exception(self):
        filename = 'test_exceptions4.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(SummingLineTypeException(5)), str(response.context['form'].errors))

    def test_bad_data_format_exception(self):
        filename = 'test_exceptions5.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(BadDataFormatException()), str(response.context['form'].errors))

    def test_preference_order_type_exception(self):
        filename = 'test_exceptions6.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(PreferenceOrderTypeException(6)), str(response.context['form'].errors))

    def test_preference_order_logic_exception(self):
        filename = 'test_exceptions7.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(PreferenceOrderLogicException(6)), str(response.context['form'].errors))

    def test_non_positive_number_of_votes_exception(self):
        filename = 'test_exceptions8.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(NonPositiveNumberOfVotesException()), str(response.context['form'].errors))

    def test_incorrect_votes_number_unique_votes_relation_exception(self):
        filename = 'test_exceptions9.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(IncorrectVotesNumberUniqueVotesRelationException()), str(response.context['form'].errors))

    def test_preference_order_length_exception(self):
        filename = 'test_exceptions10.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(PreferenceOrderLengthException()), str(response.context['form'].errors))

    def test_preference_order_beyond_scope_exception(self):
        filename = 'test_exceptions11.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(PreferenceOrderBeyondScopeException()), str(response.context['form'].errors))

    def test_incorrect_preference_order_exception(self):
        filename = 'test_exceptions12.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(IncorrectPreferenceOrderException()), str(response.context['form'].errors))

    def test_number_of_votes_inconsistency_exception(self):
        filename = 'test_exceptions13.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'input_data', filename)
        response = self.client.post(self.url, {'file': open(filename)})
        self.assertIn(str(NumberOfVotesInconsistencyException()), str(response.context['form'].errors))


class ElectionGenerateDataFormViewTestCase(TestCase):
    def setUp(self):
        self.user = self.login()
        self.election = ElectionFactory.create(user=self.user)
        self.url = reverse('elections:election_generate', args=(self.election.pk,))

    @mock.patch.object(ElectionGenerator, 'generate_elections')
    def test_form_valid_calls_run_on_algorithm(self, mocked_generate):
        data = {
            'candidates_amount': 10,
            'voters_amount': 10,
            'candidates_mean_x': 0,
            'candidates_mean_y': 0,
            'candidates_sigma': 30,
            'voters_mean_x': 0,
            'voters_mean_y': 0,
            'voters_sigma': 30,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        mocked_generate.assert_called_once()


class ElectionChartViewTest(TestCase):
    def setUp(self):
        self.file_election = ElectionFactory.create()
        self.file_cs = CandidateFactory.create_batch(4, election=self.file_election)
        self.file_vs = VoterFactory.create_batch(10, election=self.file_election)
        self.file_url = reverse('elections:chart_data', args=(self.file_election.pk,))

        self.gauss_election = ElectionFactory.create()
        self.gauss_cs = PointCandidateFactory.create_batch(4, election=self.gauss_election)
        self.gauss_vs = PointVoterFactory.create_batch(10, election=self.gauss_election)
        self.gauss_url = reverse('elections:chart_data', args=(self.gauss_election.pk,))

    def test_get_data_from_file(self):
        request = RequestFactory().get(self.file_url)
        view = ElectionChartView(request=request, election=self.file_election)
        data = view.get_data()
        candidates = data[0]
        voters = data[1]
        colors = view.get_colors()
        labels = view.get_labels()

        self.assertEqual(colors[0], 'red')
        self.assertEqual(colors[1], 'blue')
        self.assertEqual(labels[0], 'Candidates')
        self.assertEqual(labels[1], 'Voters')
        self.assertEqual(len(candidates), 0)
        self.assertEqual(len(voters), 0)

    def test_get_data_from_gauss(self):
        request = RequestFactory().get(self.gauss_url)
        view = ElectionChartView(request=request, election=self.gauss_election)
        data = view.get_data()
        candidates = data[0]
        voters = data[1]
        colors = view.get_colors()
        labels = view.get_labels()

        for point in candidates:
            self.assertTrue(isinstance(point, dict))
            self.assertIn('x', point)
            self.assertIn('y', point)

        for point in voters:
            self.assertTrue(isinstance(point, dict))
            self.assertIn('x', point)
            self.assertIn('y', point)

        self.assertEqual(colors[0], 'red')
        self.assertEqual(colors[1], 'blue')
        self.assertEqual(labels[0], 'Candidates')
        self.assertEqual(labels[1], 'Voters')
        self.assertEqual(len(candidates), 4)
        self.assertEqual(len(voters), 10)

    @mock.patch.object(ElectionChartView, 'get_labels')
    @mock.patch.object(ElectionChartView, 'get_colors')
    @mock.patch.object(ElectionChartView, 'get_points_stroke_colors')
    @mock.patch.object(ElectionChartView, 'get_data')
    def test_get_datasets(
            self, mocked_get_data, mocked_get_points_stroke_colors,
            mocked_get_colors, mocked_get_labels
    ):
        mocked_get_labels.return_value = ['label1', 'label2']
        mocked_get_colors.return_value = ['red', 'blue']
        mocked_get_points_stroke_colors.return_value = ['black', 'black']
        mocked_get_data.return_value = [[{'x': 0, 'y': 1}], [{'x': 2, 'y': 3}]]
        expected = [
            {
                "pointColor": "red",
                "pointStrokeColor": "black",
                "data": [{"x": 0, "y": 1}],
                "label": "label1"
            },
            {
                "pointColor": "blue",
                "pointStrokeColor": "black",
                "data": [{"x": 2, "y": 3}],
                "label": "label2"
            },
        ]
        request = RequestFactory().get(self.url)
        view = ElectionChartView(
            request=request,
            election=self.gauss_election
        )
        datasets = view.get_datasets()
        self.assertEqual(expected, datasets)
        response = self.client.get(self.gauss_url)
        response = json.loads(response.content)
        self.assertEqual(expected, response['data'])

    def test_dispatch_error(self):
        response = self.client.get(
            self.gauss_url.replace(str(self.gauss_election.pk), '-1')
        )
        self.assertEqual(response.status_code, 404)


class ResultChartViewTest(TestCase):
    def setUp(self):
        self.election = ElectionFactory.create()
        self.candidates = PointCandidateFactory.create_batch(4, election=self.election)
        self.voters = PointVoterFactory.create_batch(10, election=self.election)
        self.result = ResultFactory.create(election=self.election)
        self.result.winners.add(self.candidates[0])
        self.result.winners.add(self.candidates[1])
        self.url = reverse('elections:result_chart_data', args=(self.result.pk,))

    def test_get_data_from_gauss(self):
        request = RequestFactory().get(self.url)
        view = ResultChartView(
            request=request,
            election=self.election, result=self.result
        )
        data = view.get_data()
        voters = data[0]
        candidates = data[1]
        winners = data[2]
        colors = view.get_colors()
        labels = view.get_labels()

        for dataset in [candidates, voters, winners]:
            for point in dataset:
                self.assertTrue(isinstance(point, dict))
                self.assertIn('x', point)
                self.assertIn('y', point)

        for text in colors + labels:
            self.assertTrue(isinstance(text, str))

        self.assertEqual(len(candidates), 4)
        self.assertEqual(len(voters), 10)
        self.assertEqual(len(winners), 2)

    @mock.patch.object(ResultChartView, 'get_labels')
    @mock.patch.object(ResultChartView, 'get_colors')
    @mock.patch.object(ResultChartView, 'get_points_stroke_colors')
    @mock.patch.object(ResultChartView, 'get_data')
    def test_get_datasets(
            self, mocked_get_data, mocked_get_points_stroke_colors,
            mocked_get_colors, mocked_get_labels
    ):
        mocked_get_labels.return_value = ['label1', 'label2', 'label3']
        mocked_get_colors.return_value = ['red', 'blue', 'yellow']
        mocked_get_points_stroke_colors.return_value = ['black', 'black', 'black']
        mocked_get_data.return_value = [[{'x': 0, 'y': 1}], [{'x': 2, 'y': 3}], [{'x': 4, 'y': 5}]]
        expected = [
            {
                "pointColor": "red",
                "pointStrokeColor": "black",
                "data": [{"x": 0, "y": 1}],
                "label": "label1"
            },
            {
                "pointColor": "blue",
                "pointStrokeColor": "black",
                "data": [{"x": 2, "y": 3}],
                "label": "label2"
            },
            {
                "pointColor": "yellow",
                "pointStrokeColor": "black",
                "data": [{"x": 4, "y": 5}],
                "label": "label3"
            },
        ]
        request = RequestFactory().get(self.url)
        view = ResultChartView(
            request=request,
            election=self.election,
            result=self.result
        )
        datasets = view.get_datasets()
        self.assertEqual(expected, datasets)
        response = self.client.get(self.url)
        response = json.loads(response.content)
        self.assertEqual(expected, response['data'])

    def test_dispatch_error(self):
        response = self.client.get(
            self.url.replace(str(self.result.pk), '-1')
        )
        self.assertEqual(response.status_code, 404)


class ResultCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = self.login()
        self.election = ElectionFactory.create(user=self.user)
        self.url = reverse('elections:result_create', args=(self.election.pk,))

    @mock.patch.object(BruteForce, 'run')
    def test_form_valid_calls_run_on_algorithm(self, mocked_run):
        winners = [CandidateFactory.create(election=self.election)]
        mocked_run.return_value = winners
        data = {
            'p_parameter': 2,
            'algorithm': BRUTE_ALGORITHM
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        mocked_run.assert_called_once()
        result = Result.objects.get(election=self.election)
        self.assertListEqual(
            list(result.winners.all()),
            winners
        )


class ResultDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = self.login()
        self.election = ElectionFactory.create(user=self.user)
        self.result_to_delete = ResultFactory.create(election=self.election)
        self.url = reverse('elections:result_delete', args=(self.result_to_delete.pk,))

    def test_request_valid_calls_result_deleted(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_request_wrong_user_raises_404_error(self):
        self.url = reverse('elections:result_delete', args=(self.result_to_delete.pk,))

        other_user = UserFactory.create()
        other_user.set_password('secret')
        other_user.save()
        self.client.login(username=other_user.username, password='secret')

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
