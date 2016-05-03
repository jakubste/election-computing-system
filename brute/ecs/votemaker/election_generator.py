from random import gauss
from point import Point
from ecs.voter import Voter
from ecs.candidate import Candidate

import names
import config


class ElectionGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_elections(candidates_number, voters_number):
        """
        :param candidates_number:
        :param voters_number:
        :return: tuple of (list of Candidate, list of Voter)
        """
        candidates = ElectionGenerator.load_candidates(candidates_number)
        voters = ElectionGenerator.load_voters(voters_number)
        for voter in voters:
            voter.preference = ElectionGenerator.compute_preferences(voter, candidates)
        return candidates, voters

    @staticmethod
    def load_candidates(self):
        candidates = []
        for i in range(self.candidates_number):
            x = int(gauss(config.MEAN, config.SIGMA))
            y = int(gauss(config.MEAN, config.SIGMA))
            point = Point(x, y)
            name = names.get_first_name()
            candidate = Candidate(i + 1, name, point)
            candidates.append(candidate)
        return candidates

    @staticmethod
    def load_voters(self):
        voters = []
        for i in range(self.voters_number):
            x = int(gauss(config.MEAN, config.SIGMA))
            y = int(gauss(config.MEAN, config.SIGMA))
            point = Point(x, y)
            voter = Voter(1, [], point)
            voters.append(voter)
        return voters

    @staticmethod
    def compute_preferences(voter, candidates):
        """
            For each voter arranges candidates in order of euclidean norm distances
            :rtype: list of Candidates ordered by their distance from Voter
        """
        voter_preference = sorted(
            candidates,
            key=lambda candidate: Point.compute_euclidean_norm(voter.coordinates, candidate.coordinates)
        )
        return voter_preference
