from random import gauss
import config


class Population:

    def __init__(self, voters_number, candidates_number):
        self.voters_number = voters_number
        self.candidates_number = candidates_number
        self.voters_coordinates = []
        self.candidates_coordinates = []

    def generate_voters_candidates_pair(self):
        self.voters_coordinates = self.load_coordinates(self.voters_number)
        self.candidates_coordinates = self.load_coordinates(self.candidates_number)
        return self.voters_coordinates, self.candidates_coordinates

    @staticmethod
    def load_coordinates(size):
        return [(gauss(config.RANGE), gauss(config.RANGE)) for i in range(1, size)]
