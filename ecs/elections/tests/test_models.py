from ecs.elections.factories import ElectionFactory, VoterFactory, CandidateFactory, PointCandidateFactory, \
    PointVoterFactory
from ecs.utils.unittestcases import TestCase


class ElectionTestCase(TestCase):
    def test_is_set_up_flag(self):
        election = ElectionFactory.create()
        self.assertEqual(election.is_set_up(), False)
        VoterFactory.create(election=election)
        self.assertEqual(election.is_set_up(), False)
        CandidateFactory.create(election=election)
        self.assertEqual(election.is_set_up(), True)

    def test_is_set_generated_flag(self):
        empty_election = ElectionFactory.create()
        
        file_election = ElectionFactory.create()
        file_cs = CandidateFactory.create_batch(4, election=file_election)
        file_vs = VoterFactory.create_batch(10, election=file_election)

        gauss_election = ElectionFactory.create()
        gauss_cs = PointCandidateFactory.create_batch(4, election=gauss_election)
        gauss_vs = PointVoterFactory.create_batch(10, election=gauss_election)
        
        self.assertEqual(empty_election.is_generated(), False)
        self.assertEqual(file_election.is_generated(), False)
        self.assertEqual(gauss_election.is_generated(), True)
