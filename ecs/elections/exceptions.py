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


class IncorrectTypeOfCandidatesNumberException(Exception):
    def __str__(self):
        return "Incorrect type of candidates_number. Positive integer expected"


class CandidatesNameIncorrectFormatException(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return "Incorrect format of a line with candidates' name\n" + \
               "Line number in an input file: " + str(self.line_number)


class SummingLineFormatException(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return "Incorrect format of a line with number of all votes and unique votes\n" + \
               "Line number in an input file: " + str(self.line_number)


class SummingLineTypeException(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return "Incorrect type of voters_number or unique_votes. Positive integers expected\n" + \
               "Line number in an input file: " + str(self.line_number)


class PreferenceOrderTypeException(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return "Incorrect type of candidates' number in order preference or unique votes\n" + \
               "Line number in an input file: " + str(self.line_number)


class PreferenceOrderLogicException(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return "Non positive number or too big number of unique votes for an order preference" + \
               "Line number in an input file: " + str(self.line_number)
