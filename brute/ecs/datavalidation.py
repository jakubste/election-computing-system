from ecs.exceptions import NumberOfVotesInconsistencyException
from ecs.exceptions import PreferenceOrderLengthException
from ecs.exceptions import IncorrectPreferenceOrderException
from ecs.exceptions import PreferenceOrderBeyondScopeException
from ecs.exceptions import IncorrectVotesNumberUniqueVotesRelationException
from ecs.exceptions import NonPositiveNumberOfVotesException

class InputDataValidation(object):

    def __init__(self):
        super(InputDataValidation, self).__init__()

    def check_number_of_votes_consistency(self, voters_number_in_loop, voters_number_in_file_line):
        """
        check whether number of votes summed in lines of preference order is equal to number
        of votes given in a line with unique votes

        :param voters_number_in_loop: int
        :param voters_number_in_file_line: int
        :return: None
        """
        if voters_number_in_loop != voters_number_in_file_line:
            raise NumberOfVotesInconsistencyException

    def check_vote_consistency(self, preference_order, candidates_number):
        """
        check consistency of one example of preference order - checking length of preference order
        and candidates numbers presence

        :param preference_order: list
        :param candidates_number: int
        :return: None
        """
        if len(preference_order) != candidates_number:
            raise PreferenceOrderLengthException

        tmp_set = set(range(1, candidates_number + 1))
        for x in preference_order:
            if x > candidates_number or x < 1:
                raise PreferenceOrderBeyondScopeException
            try:
                tmp_set.remove(x)
            except KeyError:
                raise IncorrectPreferenceOrderException

    def check_votes_number_unique_votes_relation(self, votes_number, unique_votes):
        """
        check if number of all votes is not less than number of unique votes

        :param votes_number: int
        :param unique_votes: int
        :return: None
        """
        if votes_number <= 0 or unique_votes <= 0:
            raise NonPositiveNumberOfVotesException

        if votes_number < unique_votes:
            raise IncorrectVotesNumberUniqueVotesRelationException