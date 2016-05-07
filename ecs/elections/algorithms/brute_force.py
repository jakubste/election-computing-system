from ecs.elections.algorithms.algorithm import Algorithm


class BruteForce(Algorithm):
    def run(self, p_parameter):
        combinations = list(self.get_committee_combinations())

        winning_committee = None
        max_score = 0

        candidates_number = self.election.candidates.count()

        for committee in combinations:
            print 'committee', committee
            temp_score = 0
            for voter in self.election.voters.all():
                temp_score += voter.calculate_committee_score(committee, p_parameter, candidates_number)
            if temp_score > max_score:
                max_score = temp_score
                winning_committee = committee
        return winning_committee
