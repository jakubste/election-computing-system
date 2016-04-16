from math import sqrt
from unittest import TestCase

from ecs.votemaker.population import Population
from ecs.votemaker.preferences import Preferences
from test_data import *


class PreferencesTest(TestCase):
    def test_euclidean_norm_1(self):
        self.assertAlmostEqual(sqrt(2), Preferences.compute_euclidean_norm((0, 0), (1, 1)), 4)

    def test_euclidean_norm_2(self):
        self.assertAlmostEqual(sqrt(2), Preferences.compute_euclidean_norm((0, 0), (-1, -1)), 4)

    def test_compute_preferences_1(self):
        population_01 = Population(VOTERS_NUMBER_01, CANDIDATES_NUMBER_01)
        population_01.voters_coordinates = VOTERS_COORDINATES_01
        population_01.candidates_coordinates = CANDIDATES_COORDINATES_01
        preferences_01 = Preferences(population_01)
        preferences_01.voters_preferences = preferences_01.compute_preferences()
        self.assertListEqual(VOTERS_COORDINATES_01, population_01.voters_coordinates)
        self.assertListEqual(CANDIDATES_COORDINATES_01,
                             population_01.candidates_coordinates)
        self.assertDictEqual(PREFERENCES_01, preferences_01.voters_preferences)
