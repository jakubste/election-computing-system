import pprint

from ecs.votemaker.point import Point
from ecs.voter import Voter
from ecs.candidate import Candidate
import names
import copy

VOTERS_NUMBER_01 = 12
CANDIDATES_NUMBER_01 = 3
VOTERS_COORDINATES_01 = [(1, 5), (5, 4), (2, 3), (-3, 5), (-5, 3), (-3, 2),
                         (-3, -3), (-6, -3), (-5, -4), (2, -2), (7, -2), (2, -5)]
CANDIDATES_COORDINATES_01 = [(1, 2), (3, -1), (-2, -2)]
PREFERENCES_COORDINATES_01 = {
    (1, 5): [(1, 2), (3, -1), (-2, -2)],
    (5, 4): [(1, 2), (3, -1), (-2, -2)],
    (2, 3): [(1, 2), (3, -1), (-2, -2)],
    (-3, 5): [(1, 2), (-2, -2), (3, -1)],
    (-5, 3): [(-2, -2), (1, 2), (3, -1)],
    (-3, 2): [(1, 2), (-2, -2), (3, -1)],
    (-3, -3): [(-2, -2), (3, -1), (1, 2)],
    (-6, -3): [(-2, -2), (1, 2), (3, -1)],
    (-5, -4): [(-2, -2), (1, 2), (3, -1)],
    (2, -2): [(3, -1), (-2, -2), (1, 2)],
    (7, -2): [(3, -1), (1, 2), (-2, -2)],
    # (2, -5): [(3, -1), (1, 2), (-2, 98)]}
    (2, -5): [(3, -1), (-2, -2), (1, 2)]}


class TestDataGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_voters():
        voters = []
        for coord in VOTERS_COORDINATES_01:
            point = Point(coord[0], coord[1])
            voter = Voter(1, [], point)
            voters.append(voter)
        return voters

    @staticmethod
    def generate_candidates():
        candidates = []
        candidate_id = 1
        for coord in CANDIDATES_COORDINATES_01:
            point = Point(coord[0], coord[1])
            candidate = Candidate(candidate_id, names.get_first_name(), point)
            candidates.append(candidate)
            candidate_id += 1
        return candidates

    @staticmethod
    def get_preferences():
        voters_with_preferences = copy.deepcopy(VOTERS_WITH_NO_PREFERENCES_01)
        for voter in voters_with_preferences:
            preference = []
            pprint.pprint(PREFERENCES_COORDINATES_01)
            for coord in PREFERENCES_COORDINATES_01[(voter.coordinates.x, voter.coordinates.y)]:
                for candidate in CANDIDATES_01:
                    if (candidate.coordinates.x, candidate.coordinates.y) == coord:
                        preference.append(candidate)
                        break
            voter.preference = preference
        return CANDIDATES_01, voters_with_preferences


VOTERS_WITH_NO_PREFERENCES_01 = TestDataGenerator.generate_voters()
CANDIDATES_01 = TestDataGenerator.generate_candidates()
PREFERENCES_01 = TestDataGenerator.get_preferences()

