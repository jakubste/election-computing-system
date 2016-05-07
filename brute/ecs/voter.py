from decimal import Decimal


class Voter(object):

    preference = None

    def __init__(self, repeats=1, preference=None, coordinates=None):
        """
        :type repeats: int
        :type preference: list of ecs.candidate.Candidate
        :type coordinates: Point
        """
        self.id = id(self)
        # indicates the number of same votes in election
        self.repeats = repeats
        self.preference = preference
        self.coordinates = coordinates
        super(Voter, self).__init__()

    def __str__(self):
        return '{}x {}'.format(self.repeats, [c.candidate_id for c in self.preference])

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
    def get_candidates_by_ids(candidates, identities):
        """
        filter candidates by id in identities and order them as in identities list
        :param candidates: list (tuple) of Candidate
        :param identities: list (tuple) of int
        :return: list (tuple) of Candidate
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


