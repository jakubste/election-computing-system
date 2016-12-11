from django.conf import settings

from ecs.elections.algorithms.algorithm import Algorithm
from ecs.utils.math import ell_p_norm


class GreedyAlgorithm(Algorithm):

    def run(self):
        self.fetch_preferences()
        voters = list(self.election.voters.all())
        candidates_still_fighting = list(self.election.candidates.all())
        winning_committee = []
        actual_voters_satisfaction = {}

        for v in voters:
            actual_voters_satisfaction[v.pk] = 0

        for i in range(self.election.committee_size):
            if settings.PRINT_PROGRESS:
                print i + 1, "out of", self.election.committee_size, "to be chosen"

            satisfaction_with_leading_candidate = 0
            leading_candidate = None

            for c in candidates_still_fighting:
                satisfaction_with_given_candidate = 0

                for v in voters:
                    x = self.candidates_number - self.preferences[v.pk][c.pk]
                    satisfaction_of_given_voter = actual_voters_satisfaction[v.pk]

                    values = [satisfaction_of_given_voter, x]
                    satisfaction_of_given_voter_with_given_candidate = ell_p_norm(values, self.p_parameter)

                    satisfaction_with_given_candidate += v.repeats * satisfaction_of_given_voter_with_given_candidate

                if satisfaction_with_given_candidate > satisfaction_with_leading_candidate:
                    leading_candidate = c
                    satisfaction_with_leading_candidate = satisfaction_with_given_candidate

            self.update_voters_satisfaction(
                leading_candidate, voters, actual_voters_satisfaction, self.candidates_number, self.p_parameter
            )

            winning_committee.append(leading_candidate)
            candidates_still_fighting.remove(leading_candidate)

        return tuple(winning_committee)

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
            x = candidates_number - self.preferences[v.pk][leading_candidate.pk]
            values = [actual_voters_satisfaction[v.pk], x]
            actual_voters_satisfaction[v.pk] = ell_p_norm(values, p)
