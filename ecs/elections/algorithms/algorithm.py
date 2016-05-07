import itertools


class Algorithm(object):
    election = None

    def __init__(self, election):
        """
        :type election: ecs.elections.models.Election
        """
        self.election = election

    def get_committee_combinations(self):
        """
        :rtype: list of int
        :return: all combinations of committees in this election
        """
        combinations = itertools.combinations(
            list(self.election.candidates.all()),
            self.election.committee_size
        )
        return combinations

    def run(self, p_parameter):
        """
        Calculates winning committee of election
        :rtype: tuple of int
        """
        raise NotImplementedError
