from ecs.elections.factories import ElectionFactory, VoterFactory, CandidateFactory
from ecs.utils.unittestcases import TestCase


class ElectionTestCase(TestCase):
    def test_is_set_up_flag(self):
        election = ElectionFactory.create()
        self.assertEqual(election.is_set_up(), False)
        VoterFactory.create(election=election)
        self.assertEqual(election.is_set_up(), False)
        CandidateFactory.create(election=election)
        self.assertEqual(election.is_set_up(), True)
