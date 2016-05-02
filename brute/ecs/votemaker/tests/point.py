from math import sqrt
from unittest import TestCase
from ecs.votemaker.population import Population
from ecs.votemaker.preferences import Preferences
from test_data import *
import pprint

class PointTest(TestCase):
    def test_euclidean_norm_1(self):
        self.assertAlmostEqual(sqrt(2), Point.compute_euclidean_norm(Point(0, 0), Point(1, 1)), 4)

    def test_euclidean_norm_2(self):
        self.assertAlmostEqual(sqrt(2), Point.compute_euclidean_norm(Point(0, 0), Point(-1, -1)), 4)

    def test_compute_preferences_1(self):
        population_01 = Population(VOTERS_NUMBER_01, CANDIDATES_NUMBER_01)
        population_01.voters = VOTERS_01
        population_01.candidates = CANDIDATES_01
        preferences_01 = Preferences(population_01)
        self.assertListEqual(VOTERS_COORDINATES_01,
                             [(voter.coordinates.x, voter.coordinates.y) for voter in population_01.voters])
        for candidate in population_01.candidates:
            self.assertIn((candidate.coordinates.x, candidate.coordinates.y), CANDIDATES_COORDINATES_01)
        preferences_as_coordinates = {}
        # preferences_01.preferences - list of candidates
        for voter in preferences_01.preferences:
            preferences_as_coordinates[(voter.coordinates.x, voter.coordinates.y)] = \
                [(candidate.coordinates.x, candidate.coordinates.y) for candidate in
                 preferences_01.preferences[voter]]
        self.assertDictEqual(PREFERENCES_01, preferences_as_coordinates)
