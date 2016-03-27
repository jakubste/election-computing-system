class Vote(object):
    # indicates the number of same votes in election
    repeats = 1

    preference = []

    def __init__(self, repeats, preference):
        self.repeats = repeats
        self.preference = preference
        super(Vote, self).__init__()
