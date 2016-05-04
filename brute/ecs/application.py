from ecs.algorithms.brute_force import BruteForce
from ecs.voter import Voter
from ecs.candidate import Candidate
from ecs.exceptions import *
from ecs.datavalidation import InputDataValidation


class ElectionComputingSystem(InputDataValidation):
    algorithm = None

    candidates_number = 0
    candidates = None

    committee_size = 0

    voters_number = 0
    # to check data consistency
    unique_votes = 0
    voters = None

    p_parameter = 1

    def __init__(self, p_parameter, committee_size):
        self.committee_size = int(committee_size)
        self.p_parameter = int(p_parameter)
        self.algorithm = BruteForce(self)
        self.candidates = []
        self.voters = []
        super(ElectionComputingSystem, self).__init__()

    # moved to django
    def load_data_from_file(self, filename):
        voters_number_in_loop = 0
        election_data = open(filename, 'r')

        self.candidates_number = int(election_data.readline())
        if self.candidates_number <= 0:
            raise IncorrectTypeOfCandidatesNumberException

        # reading candidates' names
        for i in xrange(self.candidates_number):
            line = election_data.readline()
            print "lel"
            try:
                candidate_id = int(line.split(',', 1)[0].strip())
                candidate_name = line.split(',', 1)[1].strip()
            except (IndexError, ValueError):
                raise CandidatesNameIncorrectFormatException(2 + i)
            candidate = Candidate(candidate_id, candidate_name)
            self.candidates.append(candidate)

        # reading number of all votes and unique votes
        line = election_data.readline()
        line = line.split(',', 2)

        try:
            self.voters_number = int(line[1])
            self.unique_votes = int(line[2])
            self.check_votes_number_unique_votes_relation(self.voters_number, self.unique_votes)
        except IndexError:
            raise SummingLineFormatException(2 + self.candidates_number)
        except ValueError:
            raise SummingLineTypeException(2 + self.candidates_number)

        # reading order preferences
        for i in xrange(self.unique_votes):
            line = election_data.readline()
            if line == '':
                raise BadDataFormatException
            line = line.split(',', self.candidates_number)
            try:
                line = map(lambda x: int(x), line)
            except ValueError:
                raise PreferenceOrderTypeException(3 + self.candidates_number + i)
            if line[0] <= 0 or line[0] > self.voters_number:
                raise PreferenceOrderLogicException(3 + self.candidates_number + i)
            voters_number_in_loop += line[0]
            self.check_vote_consistency(line[1:], self.candidates_number)
            vote_repeats = line[0]
            # list of candidates in specified order
            preference = Voter.get_candidates_by_ids(self.candidates, line[1:])
            # arrange candidates according to preference from the file
            voter = Voter(vote_repeats, preference)
            self.voters.append(voter)

        self.check_number_of_votes_consistency(self.voters_number, voters_number_in_loop)

        print '*' * (38 + 4 + len(filename))
        print '* Successfully loaded data from file \'{}\':'.format(filename)
        print '* Candidates number:', self.candidates_number
        print '* Voters number:', self.voters_number
        print '* Unique votes:', self.unique_votes
        print '* Param p:', self.p_parameter
        print '*' * (38 + 4 + len(filename))
        print ''

        election_data.close()

    def run(self):
        winning_committee = self.algorithm.run()
        print 'Winning committee is:', winning_committee
        for candidate in winning_committee:
            print candidate, self.candidates[candidate - 1]
        print ''
