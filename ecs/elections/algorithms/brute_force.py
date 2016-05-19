from ecs.elections.algorithms.algorithm import Algorithm
from ecs.utils.math import ell_p_norm


class BruteForce(Algorithm):
    preferences = None

    def fetch_preferences(self):
        self.preferences = {}
        for voter in self.election.voters.all():
            self.preferences[voter.pk] = {}
            for preference in voter.preferences.all():
                self.preferences[voter.pk].update({
                    preference.candidate.pk: preference.preference
                })

    def calculate_committee_score_from_prefetched(self, voter, committee, p_parameter, candidates_number):

        voter_preferences = []
        for candidate in committee:
            voter_preferences.append(
                self.preferences[voter.pk][candidate.pk]
            )
        voter_preferences = [candidates_number - x for x in voter_preferences]
        return voter.repeats * ell_p_norm(voter_preferences, p_parameter)

    def run(self, p_parameter):
        combinations = list(self.get_committee_combinations())

        winning_committee = None
        max_score = 0

        candidates_number = self.election.candidates.count()
        voters = self.election.voters.all()

        self.fetch_preferences()
        num = len(combinations)

        for i, committee in enumerate(combinations):
            # print for developer - when it's running long, at least you have something to watch ;)
            print i, 'out of', num
            temp_score = 0
            for voter in voters:
                temp_score += self.calculate_committee_score_from_prefetched(
                    voter, committee, p_parameter, candidates_number
                )
            if temp_score > max_score:
                max_score = temp_score
                winning_committee = committee
        return winning_committee
