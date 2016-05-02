from random import gauss
from point import Point
from ecs.voter import Voter
from ecs.candidate import Candidate

import names
import config


class Population:

    def __init__(self, voters_number, candidates_number):
        self.voters_number = voters_number
        self.candidates_number = candidates_number
        self.voters = self.load_voters()
        self.candidates = self.load_candidates()

    def load_voters(self):
        voters = []
        for i in range(self.voters_number):
            x = int(gauss(config.MEAN, config.SIGMA))
            y = int(gauss(config.MEAN, config.SIGMA))
            point = Point(x, y)
            voter = Voter(1, [], point)
            voters.append(voter)
        return voters

    def load_candidates(self):
        candidates = []
        for i in range(self.candidates_number):
            x = int(gauss(config.MEAN, config.SIGMA))
            y = int(gauss(config.MEAN, config.SIGMA))
            point = Point(x, y)
            name = names.get_first_name()
            candidate = Candidate(i+1, name, point)
            candidates.append(candidate)
        return candidates
