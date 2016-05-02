from point import Point


class Preferences:
    def __init__(self, population):
        """
            :type population: votemaker.population.Population
        """
        self.voters = population.voters
        self.candidates = population.candidates
        self.preferences = self.compute_preferences()

    def compute_preferences(self):
        """
            For each voter arranges candidates in order of euclidean norm distances
            :rtype: dictionary, key: Voter, value: list of Candidate
        """
        voters_preferences = {}
        for voter in self.voters:
            voter_preferences = sorted(
                self.candidates,
                key=lambda candidate: Point.compute_euclidean_norm(voter.coordinates, candidate.coordinates)
            )
            voters_preferences[voter] = voter_preferences
        return voters_preferences


