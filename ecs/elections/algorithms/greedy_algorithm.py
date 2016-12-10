from ecs.elections.algorithms.algorithm import Algorithm
from ecs.utils.math import ell_p_norm


class GreedyAlgorithm(Algorithm):
    preferences = None

    def fetch_preferences(self):
        self.preferences = {}
        for voter in self.election.voters.all().prefetch_related('preferences__candidate'):
            self.preferences[voter.pk] = {}
            for preference in voter.preferences.all():
                self.preferences[voter.pk].update({
                    preference.candidate.pk: preference.preference
                })

    def run(self):

        voters = self.election.voters.all()
        candidates_number = self.election.candidates.count()

        self.fetch_preferences()
        candidates_still_fighting = self.election.candidates.all()
        winning_committee = []
        actual_voters_satisfaction = {}

        for v in voters:
            actual_voters_satisfaction[v.pk] = 0

        for i in range(self.election.committee_size):
            print i + 1, "out of", self.election.committee_size, "to be chosen"
            satisfaction_with_leading_candidate = 0
            leading_candidate = None
            for c in candidates_still_fighting:
                satisfaction_with_given_candidate = 0
                for v in voters:
                    x = self.number_of_points_in_preference_order(c, v, candidates_number)
                    satisfaction_of_given_voter = \
                        self.get_actual_satisfaction_of_given_voter(v, actual_voters_satisfaction)

                    values = [satisfaction_of_given_voter, x]
                    satisfaction_of_given_voter_with_given_candidate = ell_p_norm(values, self.p_parameter)

                    satisfaction_with_given_candidate += v.repeats * satisfaction_of_given_voter_with_given_candidate

                if satisfaction_with_given_candidate > satisfaction_with_leading_candidate:
                    leading_candidate = c
                    satisfaction_with_leading_candidate = satisfaction_with_given_candidate
            self.update_voters_satisfaction(leading_candidate, voters, actual_voters_satisfaction, candidates_number,
                                            self.p_parameter)
            winning_committee.append(leading_candidate)
            candidates_still_fighting = candidates_still_fighting.exclude(pk=leading_candidate.pk)

        return tuple(winning_committee)

    def number_of_points_in_preference_order(self, c, v, candidates_number):
        """
        :param c: Candidate
        :param candidates_number: int
        :param v: Voter
        :return: int
        """

        return candidates_number - self.preferences[v.pk][c.pk]

    @staticmethod
    def get_actual_satisfaction_of_given_voter(v, actual_voters_satisfaction):
        """
        :param actual_voters_satisfaction: int
        :param v: Voter
        :return: int
        """
        return actual_voters_satisfaction[v.pk]

    def update_voters_satisfaction(self, leading_candidate, voters, actual_voters_satisfaction, candidates_number, p):
        """
        :param leading_candidate: Candidate
        :param voters: QuerySet
        :param actual_voters_satisfaction: dict{Voter: int}
        :param candidates_number: int
        :param p: int
        :return:
        """
        for v in voters:
            x = self.number_of_points_in_preference_order(leading_candidate, v, candidates_number)
            values = [actual_voters_satisfaction[v.pk], x]
            actual_voters_satisfaction[v.pk] = ell_p_norm(values, p)
