class BadDataFormatException(Exception):
    def __str__(self):
        return 'Empty line instead of vote data'


class NumberOfVotesInconsistencyException(Exception):
    def __str__(self):
        return 'Summed number of votes differs from the expected given in summarizing line'


class PreferenceOrderLengthException(Exception):
    def __str__(self):
        return 'Number of candidates in preference order is not equal to number of candidates'