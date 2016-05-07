from ecs.elections.algorithms.algorithm import Algorithm
from ecs.elections.factories import ElectionFactory, CandidateFactory
from ecs.utils.unittestcases import TestCase


class AlgorithmTestCase(TestCase):
    def setUp(self):
        self.election = ElectionFactory.create(committee_size=2)
        CandidateFactory.create_batch(3, election=self.election)
        self.algorithm = Algorithm(self.election)

    def test_get_combinations(self):
        self.assertEqual(
            len(list(self.algorithm.get_committee_combinations())),
            3
        )

    def test_run_raises_not_implemented_error(self):
        self.assertRaises(
            NotImplementedError,
            self.algorithm.run,
            (2, )
        )
