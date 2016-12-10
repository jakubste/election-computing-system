import itertools
from datetime import datetime

from ecs.utils.math import ell_p_norm


class Algorithm(object):
    election = None
    candidates_number = 0
    voters = None
    biggest = 0

    def __init__(self, election, p_parameter):
        """
        :type election: ecs.elections.models.Election
        """
        self.election = election
        self.candidates_number = self.election.candidates.count()
        self.voters = self.election.voters.all()
        self.p_parameter = p_parameter
        self.preferences = None

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

    def start(self):
        start_time = datetime.now()
        result = self.run()
        end_time = datetime.now()
        time = end_time - start_time
        return time.total_seconds(), result

    def run(self):
        """
        Calculates winning committee of election
        :rtype: tuple of int
        """
        raise NotImplementedError

    def fetch_preferences(self):
        self.preferences = {}
        for voter in self.election.voters.all().prefetch_related('preferences__candidate'):
            self.preferences[voter.pk] = {}
            for preference in voter.preferences.all():
                self.preferences[voter.pk].update({
                    preference.candidate.pk: preference.preference
                })

    def calculate_committee_score_from_prefetched(self, committee):
        temp_score = 0
        for voter in self.voters:
            voter_preferences = []
            for candidate in committee:
                voter_preferences.append(
                    self.preferences[voter.pk][candidate.pk]
                )
            voter_preferences = [self.candidates_number - x for x in voter_preferences]
            temp_score += voter.repeats * ell_p_norm(voter_preferences, self.p_parameter)
        if temp_score > self.biggest:
            self.biggest = temp_score
        return temp_score
