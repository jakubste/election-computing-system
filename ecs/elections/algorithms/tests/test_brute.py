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
        self.algorithm = BruteForce(self.election)

    @mock.patch.object(Voter, 'calculate_committee_score')
    def test_run_calls_calculate_committee_score(self, mocked_score):
        self.algorithm.run(2)
        self.assertEqual(
            mocked_score.call_count,
            3*3
        )

    def test_run_returns_winners(self):
        self.assertEqual(
            list(self.algorithm.run(2)),
            self.candidates[:2]
        )

