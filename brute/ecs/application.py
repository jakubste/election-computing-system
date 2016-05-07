from ecs.algorithms.brute_force import BruteForce
from ecs.voter import Voter
from ecs.candidate import Candidate
from ecs.exceptions import *
from ecs.datavalidation import InputDataValidation


class ElectionComputingSystem(InputDataValidation):
    algorithm = None

    candidates_number = 0
    candidates = None

    committee_size = 0

    voters_number = 0
    # to check data consistency
    unique_votes = 0
    voters = None

    p_parameter = 1

    def __init__(self, p_parameter, committee_size):
        self.committee_size = int(committee_size)
        self.p_parameter = int(p_parameter)
        self.algorithm = BruteForce(self)
        self.candidates = []
        self.voters = []
        super(ElectionComputingSystem, self).__init__()
