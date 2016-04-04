import itertools


class Algorithm(object):
    elections = None

    def __init__(self, elections):
        """
        :type elections: ecs.application.ElectionComputingSystem
        """
        self.elections = elections

    def get_committee_combinations(self):
        """
        :rtype: list of int
        :return: all combinations of committees in this elections
        """
        combinations = itertools.combinations(
            range(1, self.elections.candidates_number + 1),
            self.elections.committee_size
        )
        return combinations

    def run(self):
        """
        Calculates winning committee of elections
        :rtype: tuple of int
        """
        raise NotImplementedError
