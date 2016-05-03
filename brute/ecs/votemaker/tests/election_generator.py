from math import sqrt
from unittest import TestCase
import mock
from ecs.votemaker.election_generator import ElectionGenerator
from test_data import *

mock.patch.object = mock.patch.object


class ElectionGeneratorTest(TestCase):
    @mock.patch.object(ElectionGenerator, 'load_candidates')
    @mock.patch.object(ElectionGenerator, 'load_voters')
    def test_compute_preferences_1(self, mocked_load_voters, mocked_load_candidates):
        mocked_load_voters.return_value = VOTERS_WITH_NO_PREFERENCES_01
        mocked_load_candidates.return_value = CANDIDATES_01
        expected_preferences = PREFERENCES_01

        result_preferences = ElectionGenerator.generate_elections(CANDIDATES_NUMBER_01, VOTERS_NUMBER_01)
        result_candidates = result_preferences[0]
        # voters with set up preferences
        result_voters = result_preferences[1]

        # self.maxDiff = None
        self.assertListEqual(CANDIDATES_COORDINATES_01,
                             [(candidate.coordinates.x, candidate.coordinates.y) for candidate in result_candidates])
        self.assertListEqual(VOTERS_COORDINATES_01,
                             [(voter.coordinates.x, voter.coordinates.y) for voter in result_voters])

        self.assertEqual(expected_preferences[0], result_preferences[0])

        for expected_voter, result_voter in zip(expected_preferences[1], result_preferences[1]):
            self.assertListEqual(expected_voter.preference, result_voter.preference)
