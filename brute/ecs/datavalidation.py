from ecs.exceptions import NumberOfVotesInconsistencyException
from ecs.exceptions import PreferenceOrderLengthException

class InputDataValidation(object):

    def __init__(self):
        super(InputDataValidation, self).__init__()

    def check_number_of_votes_consistency(self, voters_number_in_loop, voters_number_in_file_line):
        if voters_number_in_loop != voters_number_in_file_line:
            raise NumberOfVotesInconsistencyException

    def check_vote_consistency(self, preference_order, candidates_number):
        if len(preference_order) != candidates_number:
            raise PreferenceOrderLengthException