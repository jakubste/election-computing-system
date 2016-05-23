import mock

from ecs.elections.algorithms.brute_force import BruteForce
from ecs.elections.factories import ElectionFactory, CandidateFactory, VoterFactory, PreferenceFactory
from ecs.elections.models import Voter
from ecs.utils.unittestcases import TestCase

mock.patch.object = mock.patch.object


class BruteForceAlgorithmTestCase(TestCase):
    def setUp(self):
        self.election = ElectionFactory.create(committee_size=2)
        self.candidates = CandidateFactory.create_batch(3, election=self.election)
        self.voters = VoterFactory.create_batch(3, election=self.election)
        for voter in self.voters:
            for candidate in self.candidates:
                PreferenceFactory.create(
                    voter=voter, candidate=candidate
                )
        self.p_parameter = 2
        self.algorithm = BruteForce(self.election, self.p_parameter)

    @mock.patch.object(BruteForce, 'calculate_committee_score_from_prefetched')
    def test_run_calls_calculate_committee_score(self, mocked_score):
        self.algorithm.run()
        self.assertEqual(
            mocked_score.call_count,
            3
        )

    def test_run_returns_winners(self):
        self.assertEqual(
            list(self.algorithm.run()),
            self.candidates[:2]
        )

    def test_start_returns_time_and_winners(self):
        time, winners = self.algorithm.start()
        winners = list(winners)
        self.assertEqual(
            winners,
            self.candidates[:2]
        )
        self.assertGreater(time, 0)
