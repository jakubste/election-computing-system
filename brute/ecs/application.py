from ecs.exceptions import BadDataFormatException
from ecs.vote import Vote


class ElectionComputingSystem(object):
    candidates_number = 0
    candidates = []

    voters_number = 0
    unique_votes = 0
    votes = []

    p_parameter = 1

    def __init__(self, p_parameter):
        self.p_parameter = p_parameter
        super(ElectionComputingSystem, self).__init__()

    def load_data_from_file(self, filename):
        election_data = open(filename, 'r')

        self.candidates_number = int(election_data.readline())

        for i in xrange(self.candidates_number):
            line = election_data.readline()
            candidate_name = line.split(',', 1)[1]
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

        print 'Successfully loaded data from file \'{}\':'.format(filename)
        print 'Candidates number:', self.candidates_number
        print 'Voters number:', self.voters_number
        print 'Unique votes:', self.unique_votes
        print 'Param p:', self.p_parameter
        print ''

        election_data.close()

    def run(self):
        pass
