from unittest import TestCase

from ecs.votemaker.population import Population


class PopulationTest(TestCase):
    def test_population(self):
        population_01 = Population(10, 3)
        self.assertTrue(len(population_01.voters) == 10)
        self.assertTrue(len(population_01.candidates) == 3)

