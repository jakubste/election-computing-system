from ecs.algorithms.brute_force import BruteForce
from ecs.exceptions import BadDataFormatException
from ecs.vote import Vote
from ecs.datavalidation import InputDataValidation


class ElectionComputingSystem(object):
    algorithm = None

    candidates_number = 0
    candidates = None

    committee_size = 0

    voters_number = 0
    # to check data consistency
    voters_number_in_loop = 0
    unique_votes = 0
    votes = None

    p_parameter = 1

    def __init__(self, p_parameter, committee_size):
        self.committee_size = int(committee_size)
        self.p_parameter = int(p_parameter)
        self.algorithm = BruteForce(self)
        self.candidates = []
        self.votes = []
        super(ElectionComputingSystem, self).__init__()

    def load_data_from_file(self, filename):
        input_data_validation = InputDataValidation()
        election_data = open(filename, 'r')

        # reading number of candidates
        try:
            self.candidates_number = int(election_data.readline())
            if self.candidates_number <= 0:
                raise ValueError
        except ValueError:
            print "Incorrect type of candidates_number. Positive integer expected"
            raise

        # reading candidates' names
        for i in xrange(self.candidates_number):
            line = election_data.readline()
            try:
                candidate_name = line.split(',', 1)[1].strip()
            except IndexError:
                print "Incorrect format of a line with candidates' name"
                print "Line number in an input file:", 2 + i
                raise
            self.candidates.append(candidate_name)

        # reading number of all votes and unique votes
        line = election_data.readline()
        line = line.split(',', 2)

        try:
            self.voters_number = int(line[1])
            self.unique_votes = int(line[2])
            input_data_validation.check_votes_number_unique_votes_relation(self.voters_number, self.unique_votes)
        except IndexError:
            print "Incorrect format of a line with number of all votes and unique votes"
            print "Line number in an input file:", 2 + self.candidates_number
            raise
        except ValueError:
            print "Incorrect type of voters_number or unique_votes. Positive integers expected"
            print "Line number in an input file:", 2 + self.candidates_number
            raise

        # reading order preferences
        for i in xrange(self.unique_votes):
            line = election_data.readline()
            if line == '':
                raise BadDataFormatException
            line = line.split(',', self.candidates_number)
            try:
                line = map(lambda x: int(x), line)
            except ValueError:
                print "Incorrect type of candidates' number in order preference or unique votes"
                print "Line number in an input file:", 3 + self.candidates_number + i
                raise
            if line[0] <= 0 or line[0] > self.voters_number:
                print "Non positive number or too big number of unique votes for an order preference"
                print "Line number in an input file:", 3 + self.candidates_number + i
                raise ValueError
            self.voters_number_in_loop += line[0]
            input_data_validation.check_vote_consistency(line[1:], self.candidates_number)
            vote = Vote(line[0], line[1:])
            self.votes.append(vote)

        input_data_validation.check_number_of_votes_consistency(self.voters_number, self.voters_number_in_loop)

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
