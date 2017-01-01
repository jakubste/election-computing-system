import mock

from ecs.elections.algorithms.greedy_cc import GreedyCC
from ecs.elections.factories import ElectionFactory, CandidateFactory, VoterFactory, PreferenceFactory
from ecs.utils.unittestcases import TestCase

mock.patch.object = mock.patch.object


class GreedyCCTestCase(TestCase):
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
        self.algorithm = GreedyCC(self.election, 2)

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
