import unittest
from votemaker.population import Population


class PopulationTest(unittest.TestCase):
    def test_population(self):
        population_01 = Population(10, 3)
        self.assertTrue(population_01.voters_coordinates.__sizeof__() == 10)
        self.assertTrue(population_01.candidates_coordinates.__sizeof__() == 3)

if __name__ == '__main__':
    unittest.main()
