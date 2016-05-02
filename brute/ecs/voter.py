from decimal import Decimal


class Voter(object):
    # indicates the number of same votes in election
    repeats = 1

    preference = None

    def __init__(self, repeats, preference):
        """
        :type repeats: int
        :type preference: list of ecs.candidate.Candidate
        """
        self.repeats = repeats
        self.preference = preference
        super(Voter, self).__init__()

    def __str__(self):
        return '{}x {}'.format(self.repeats, [c.candidate_id for c in self.preference])

    @staticmethod
    def ell_p_norm(values, p):
        """
        Returns ell_p norm of values

        :type values: list of int
        :type p: int
        :rtype: Decimal
        """
        values = map(lambda x: x ** p, values)
        value = reduce(lambda x, y: x + y, values)
        value = Decimal(value) ** Decimal(1.0 / p)
        return value

    def calculate_committee_score(self, committee, p):
        """
        Calculate committee score multiplied by vote repeats

        :param committee: list of ecs.candidate.Candidate
        :param p: int
        :rtype: Decimal
        :return: committee score
        """
        candidates_number = len(self.preference)
        # create pos_v sequence, but order actually
        # does not matter in our election system:
        committee = map(
            lambda x:  self.preference.index(x) + 1,
            committee
        )
        committee = map(
            lambda x: candidates_number - x,
            committee
        )
        return self.repeats * self.ell_p_norm(committee, p)

    @staticmethod
    def order_candidates_by_ids(candidates, identities):
        """
        converts list (tuple) of int to list (tuple) of Candidate
        :param candidates: list (tuple) of Candidate
        :param identities: list (tuple) of int
        :return: list of Candidate ordered by identities
        """
        preference = []
        for candidate_id in identities:
            preference.append(
                next(
                    (candidate for candidate in candidates
                     if candidate.candidate_id == candidate_id), None
                )
            )
        if type(identities) is list:
            return preference
        else:
            return tuple(preference)


