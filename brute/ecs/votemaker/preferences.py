from math import sqrt


class Preferences:
    def __init__(self, population):
        """
            :type population: votemaker.population.Population
        """
        self.voters_coordinates = population.voters_coordinates
        self.candidates_coordinates = population.candidates_coordinates
        self.voters_preferences = self.compute_preferences()

    def compute_preferences(self):
        """
            For each voter arranges candidates in order of euclidean norm distances
            :rtype: dictionary, key: tuple of double, value: list of tuples of double
        """
        voters_preferences = {}
        for voter in self.voters_coordinates:
            voter_preferences = sorted(
                self.candidates_coordinates,
                key=lambda candidate: self.compute_euclidean_norm(voter, candidate)
            )
            voters_preferences[voter] = voter_preferences
        return voters_preferences

    @staticmethod
    def compute_euclidean_norm((x1, y1), (x2, y2)):
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
