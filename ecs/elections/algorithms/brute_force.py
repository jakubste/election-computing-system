from ecs.elections.algorithms.algorithm import Algorithm


class BruteForce(Algorithm):
    preferences = None

    def run(self):
        combinations = list(self.get_committee_combinations())

        winning_committee = None
        max_score = 0


        self.fetch_preferences()
        num = len(combinations)

        for i, committee in enumerate(combinations):
            # print for developer - when it's running long, at least you have something to watch ;)
            print i, 'out of', num
            score = self.calculate_committee_score_from_prefetched(
                committee
            )
            if score > max_score:
                max_score = score
                winning_committee = committee
        return winning_committee
