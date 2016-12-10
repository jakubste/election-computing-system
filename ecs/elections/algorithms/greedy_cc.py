from ecs.elections.algorithms.algorithm import Algorithm


class GreedyCC(Algorithm):
    preferences = None

    def fetch_preferences(self):
        self.preferences = {}
        for voter in self.election.voters.all().prefetch_related('preferences__candidate'):
            self.preferences[voter.pk] = {}
            for preference in voter.preferences.all():
                self.preferences[voter.pk].update({
                    preference.candidate.pk: preference.preference
                })

    def run(self, p_parameter):
        voters = self.election.voters.all()
        candidates_number = self.election.candidates.count()

        self.fetch_preferences()
        candidates_still_fighting = self.election.candidates.all()
        winning_committee = []
        actual_voters_satisfaction = {}

        for v in voters:
            actual_voters_satisfaction[v.pk] = 0

        for i in range(self.election.committee_size):
            extra_satisfaction_with_leading_candidate = 0
            leading_candidate = None
            for c in candidates_still_fighting:
                extra_satisfaction_with_given_candidate = 0
                for v in voters:
                    x = self.number_of_points_in_preference_order(c, v, candidates_number)
                    satisfaction_of_given_voter = self.get_actual_satisfaction_of_given_voter(v,
                                                                                              actual_voters_satisfaction)

                    if x > satisfaction_of_given_voter:
                        extra_satisfaction_with_given_candidate += v.repeats * (
                        x - satisfaction_of_given_voter)

                if extra_satisfaction_with_given_candidate > extra_satisfaction_with_leading_candidate:
                    leading_candidate = c
                    extra_satisfaction_with_leading_candidate = extra_satisfaction_with_given_candidate

            for v in voters:
                x = self.number_of_points_in_preference_order(leading_candidate, v, candidates_number)
                if x > actual_voters_satisfaction[v.pk]:
                    actual_voters_satisfaction[v.pk] = x
            winning_committee.append(leading_candidate)
            candidates_still_fighting = candidates_still_fighting.exclude(pk=leading_candidate.pk)

        return tuple(winning_committee)

    def number_of_points_in_preference_order(self, c, v, candidates_number):
        """

        :param v: Voter, c: Candidate, candidates_number: int
        :return: int
        """

        return candidates_number - self.preferences[v.pk][c.pk]

    def get_actual_satisfaction_of_given_voter(self, v, actual_voters_satisfaction):
        """

        :param v: Voter
        :return: int
        """
        return actual_voters_satisfaction[v.pk]

