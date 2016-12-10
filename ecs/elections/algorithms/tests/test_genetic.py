import mock

from ecs.elections.algorithms.brute_force import BruteForce
from ecs.elections.algorithms.genetic import GeneticAlgorithm, Individual
from ecs.elections.factories import ElectionFactory, CandidateFactory, VoterFactory, PreferenceFactory
from ecs.utils.unittestcases import TestCase

mock.patch.object = mock.patch.object


class GeneticAlgorithmTestCase(TestCase):
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
        self.cycles = 10
        self.algorithm = GeneticAlgorithm(self.election, self.p_parameter, **{
            'mutation_probability': 10,
            'crossing_probability': 10,
            'cycles': self.cycles,
        })

    @mock.patch.object(Individual, 'mutate')
    def test_run_calls_mutate(self, mocked_mutate):
        mocked_mutate.return_value = None
        self.algorithm.run()
        self.assertGreater(mocked_mutate.call_count, 1)

    def test_run_returns_winners(self):
        self.assertItemsEqual(
            list(self.algorithm.run()),
            self.candidates[:2]
        )

    def test_start_returns_time_and_winners(self):
        time, winners = self.algorithm.start()
        winners = list(winners)
        self.assertItemsEqual(
            winners,
            self.candidates[:2]
        )
        self.assertGreater(time, 0)
