class BadDataFormatException(Exception):
    def __str__(self):
        return 'Empty line instead of vote data'


class NumberOfVotesInconsistencyException(Exception):
    def __str__(self):
        return 'Summed number of votes differs from the expected given in summarizing line'


class PreferenceOrderLengthException(Exception):
    def __str__(self):
        return 'Number of candidates in preference order is not equal to number of candidates'


class IncorrectPreferenceOrderException(Exception):
    def __str__(self):
        return "Error of votes' preference order"


class PreferenceOrderBeyondScopeException(Exception):
    def __str__(self):
        return "In votes' preference order, one of the candidates' number is beyond expected scope"


class IncorrectVotesNumberUniqueVotesRelationException(Exception):
    def __str__(self):
        return "Number of all votes must be greater or equal to unique votes"


class NonPositiveNumberOfVotesException(Exception):
    def __str__(self):
        return "Non positive number of voters_number or unique_votes. Positive integers expected"