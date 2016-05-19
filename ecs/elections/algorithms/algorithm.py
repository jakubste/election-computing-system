import itertools
from datetime import datetime


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

    def start(self, p_parameter):
        start_time = datetime.now()
        result = self.run(p_parameter)
        end_time = datetime.now()
        time = end_time - start_time
        return time.total_seconds(), result

    def run(self, p_parameter):
        """
        Calculates winning committee of election
        :rtype: tuple of int
        """
        raise NotImplementedError
