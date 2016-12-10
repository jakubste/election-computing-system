from ecs.elections.algorithms.algorithm import Algorithm


class GreedyCC(Algorithm):

    def run(self):
        voters = self.election.voters.all()

        self.fetch_preferences()
        candidates_still_fighting = list(self.election.candidates.all())
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
                    x = self.candidates_number - self.preferences[v.pk][c.pk]
                    satisfaction_of_given_voter = actual_voters_satisfaction[v.pk]

                    if x > satisfaction_of_given_voter:
                        extra_satisfaction_with_given_candidate += v.repeats * (
                            x - satisfaction_of_given_voter)

                if extra_satisfaction_with_given_candidate > extra_satisfaction_with_leading_candidate:
                    leading_candidate = c
                    extra_satisfaction_with_leading_candidate = extra_satisfaction_with_given_candidate

            for v in voters:
                x = self.candidates_number - self.preferences[v.pk][leading_candidate.pk]
                if x > actual_voters_satisfaction[v.pk]:
                    actual_voters_satisfaction[v.pk] = x

            winning_committee.append(leading_candidate)
            candidates_still_fighting.remove(leading_candidate)

        return tuple(winning_committee)
