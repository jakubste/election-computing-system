import mock

from ecs.elections.algorithms.greedy_algorithm import GreedyAlgorithm
from ecs.elections.factories import ElectionFactory, CandidateFactory, VoterFactory, PreferenceFactory
from ecs.utils.unittestcases import TestCase

mock.patch.object = mock.patch.object


class GreedyAlgorithmTestCase(TestCase):
    def setUp(self):
        self.election = ElectionFactory.create(committee_size=2)
        self.candidates = CandidateFactory.create_batch(3, election=self.election)
        self.voters = VoterFactory.create_batch(3, election=self.election)
        self.satisfaction = {}
        for voter in self.voters:
            self.satisfaction[voter.pk] = 56
            for candidate in self.candidates:
                PreferenceFactory.create(
                    voter=voter, candidate=candidate
                )
        self.algorithm = GreedyAlgorithm(self.election)

    def test_run_returns_winners(self):
        self.assertEqual(
            list(self.algorithm.run(2)),
            self.candidates[:2]
        )

    def test_start_returns_time_and_winners(self):
        time, winners = self.algorithm.start(2)
        winners = list(winners)
        self.assertEqual(
            winners,
            self.candidates[:2]
        )
        self.assertGreater(time, 0)

    @mock.patch.object(GreedyAlgorithm, 'update_voters_satisfaction')
    def test_run_calls_update_voters_satisfaction(self, updated_satisfaction):
        self.algorithm.run(2)
        self.assertEqual(
            updated_satisfaction.call_count,
            2
        )

    @mock.patch.object(GreedyAlgorithm, 'number_of_points_in_preference_order')
    def test_run_calls_number_of_points_in_preference_order(self, points_number):
        points_number.return_value = 1234
        self.algorithm.run(2)
        self.assertEqual(
            points_number.call_count,
            21
        )

    @mock.patch.object(GreedyAlgorithm, 'get_actual_satisfaction_of_given_voter')
    def test_run_calls_get_actual_satisfaction_of_given_voter(self, satisfaction):
        satisfaction.return_value = 1234
        self.algorithm.run(2)
        self.assertEqual(
            satisfaction.call_count,
            15
        )

    @mock.patch.object(GreedyAlgorithm, 'number_of_points_in_preference_order')
    def test_update_voters_satisfaction_calls_number_of_points_in_preference_order(self, satisfaction_update):
        satisfaction_update.return_value = 1234
        self.algorithm.update_voters_satisfaction(leading_candidate=self.candidates[1], voters=self.voters,
                                                  actual_voters_satisfaction=self.satisfaction,
                                                  candidates_number=3,
                                                  p=2)
        self.assertEqual(
            satisfaction_update.call_count,
            3
        )
