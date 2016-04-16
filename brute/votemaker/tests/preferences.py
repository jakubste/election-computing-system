import unittest
from votemaker.preferences import Preferences
from votemaker.population import Population
from test_data import *
from math import sqrt


class PreferencesTest(unittest.TestCase):

    def test_euclidean_norm_1(self):
        self.assertAlmostEqual(sqrt(2), Preferences.compute_euclidean_norm((0, 0), (1, 1)), 4)

    def test_euclidean_norm_2(self):
        self.assertAlmostEqual(sqrt(2), Preferences.compute_euclidean_norm((0, 0), (-1, -1)), 4)

    def test_compute_preferences_1(self):
        population_01 = Population(12, 3)
        population_01.voters_coordinates = VOTERS_COORDINATES_01
        population_01.candidates_coordinates = CANDIDATES_COORDINATES_01
        preferences_01 = Preferences(population_01)
        preferences_01.voters_preferences = preferences_01.compute_preferences()
        self.assertListEqual(VOTERS_COORDINATES_01, population_01.voters_coordinates, "voters_coordinates - OK")
        self.assertListEqual(CANDIDATES_COORDINATES_01,
                             population_01.candidates_coordinates, "candidates_coordinates - OK")
        self.assertDictEqual(PREFERENCES_01, preferences_01.voters_preferences, "preferences_01 - OK")
