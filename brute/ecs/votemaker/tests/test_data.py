from ecs.votemaker.point import Point
from ecs.voter import Voter
from ecs.candidate import Candidate
import names

VOTERS_NUMBER_01 = 12
CANDIDATES_NUMBER_01 = 3
VOTERS_COORDINATES_01 = [(1, 5), (5, 4), (2, 3), (-3, 5), (-5, 3), (-3, 2),
                         (-3, -3), (-6, -3), (-5, -4), (2, -2), (7, -2), (2, -5)]
CANDIDATES_COORDINATES_01 = [(1, 2), (3, -1), (-2, -2)]
PREFERENCES_01 = {
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
    (2, -5): [(3, -1), (-2, -2), (1, 2)]}


def generate_voters():
    voters = []
    for coord in VOTERS_COORDINATES_01:
        point = Point(coord[0], coord[1])
        voter = Voter(1, [], point)
        voters.append(voter)
    return voters


def generate_candidates():
    candidates = []
    candidate_id = 1
    for coord in CANDIDATES_COORDINATES_01:
        point = Point(coord[0], coord[1])
        candidate = Candidate(candidate_id, names.get_first_name(), point)
        candidates.append(candidate)
        candidate_id += 1
    return candidates

VOTERS_01 = generate_voters()
CANDIDATES_01 = generate_candidates()







