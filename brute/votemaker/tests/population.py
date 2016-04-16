import unittest
from votemaker.population import Population


class PopulationTest(unittest.TestCase):
    def test_population(self):
        population_01 = Population(10, 3)
        self.assertTrue(len(population_01.voters_coordinates) == 10)
        self.assertTrue(len(population_01.candidates_coordinates) == 3)

