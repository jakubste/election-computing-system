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
