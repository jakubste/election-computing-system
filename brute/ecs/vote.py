class Vote(object):
    # indicates the number of same votes in election
    repeats = 1

    preference = []

    def __init__(self, repeats, preference):
        self.repeats = repeats
        self.preference = preference
        super(Vote, self).__init__()

    @staticmethod
    def ell_p_norm(p, values):
        values = map(lambda x: x**p, values)
        value = reduce(lambda x, y: x+y, values)
        try:
            return pow(value, 1.0/p)
            # pow() implementation casts value to float format
            # This means if we want calculate root of number
            # that is bigger than float max we need to do it
            # different way
        except OverflowError:
            return -1
            pass

    def calculate_committee_score(self, committee, p):
        pass
