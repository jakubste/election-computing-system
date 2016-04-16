from random import gauss

import config


class Population:

    def __init__(self, voters_number, candidates_number):
        self.voters_number = voters_number
        self.candidates_number = candidates_number
        self.voters_coordinates = self.load_coordinates(self.voters_number)
        self.candidates_coordinates = self.load_coordinates(self.candidates_number)

    @staticmethod
    def load_coordinates(size):
        return [(int(gauss(config.MEAN, config.SIGMA)), int(gauss(config.MEAN, config.SIGMA))) for i in range(0, size)]
