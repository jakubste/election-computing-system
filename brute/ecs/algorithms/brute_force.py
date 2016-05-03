from ecs.algorithms.algorithm import Algorithm


class BruteForce(Algorithm):
    def run(self):
        combinations = list(self.get_committee_combinations())

        winning_committee = None
        max_score = 0

        for committee in combinations:
            temp_score = 0
            for voter in self.elections.voters:
                temp_score += voter.calculate_committee_score(committee, self.elections.p_parameter)
            if temp_score > max_score:
                max_score = temp_score
                winning_committee = committee
        return winning_committee
