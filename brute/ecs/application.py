from ecs.algorithms.brute_force import BruteForce
from ecs.exceptions import BadDataFormatException
from ecs.vote import Vote


class ElectionComputingSystem(object):
    algorithm = None

    candidates_number = 0
    candidates = []

    committee_size = 0

    voters_number = 0
    unique_votes = 0
    votes = []

    p_parameter = 1

    def __init__(self, p_parameter, committee_size):
        self.committee_size = int(committee_size)
        self.p_parameter = int(p_parameter)
        self.algorithm = BruteForce(self)
        super(ElectionComputingSystem, self).__init__()

    def load_data_from_file(self, filename):
        election_data = open(filename, 'r')

        self.candidates_number = int(election_data.readline())

        for i in xrange(self.candidates_number):
            line = election_data.readline()
            candidate_name = line.split(',', 1)[1].strip()
            self.candidates.append(candidate_name)

        line = election_data.readline()
        line = line.split(',', 2)
        self.voters_number = int(line[1])
        self.unique_votes = int(line[2])

        for i in xrange(self.unique_votes):
            line = election_data.readline()
            if line == '':
                raise BadDataFormatException
            line = line.split(',', self.candidates_number)
            line = map(lambda x: int(x), line)
            vote = Vote(line[0], line[1:])
            self.votes.append(vote)

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
