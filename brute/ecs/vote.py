from decimal import Decimal


class Vote(object):
    # indicates the number of same votes in election
    repeats = 1

    preference = None

    def __init__(self, repeats, preference):
        """
        :type repeats: int
        :type preference: list of int
        """
        self.repeats = repeats
        self.preference = preference
        super(Vote, self).__init__()

    def __str__(self):
        return '{}x {}'.format(self.repeats, self.preference)

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

        :param committee: list of ints
        :param p: int
        :rtype: Decimal
        :return: committee score
        """
        candidates_number = len(self.preference)
        # create pos_v sequence, but order actually
        # does not matter in our election system:
        committee = map(
            lambda x: (self.preference.index(x) + 1),
            committee
        )
        committee = map(
            lambda x: candidates_number - x,
            committee
        )
        return self.repeats * self.ell_p_norm(committee, p)
