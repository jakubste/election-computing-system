import random as r


class Population:

    def __init__(self, voters_number, candidates_number):
        self.v = voters_number
        self.c = candidates_number
        self.v_coord = []
        self.c_coord = []

    def generate_voters(self):
        self.v_coord = [[r.uniform(1, 1000)
                       for i in range(1, self.v)]
                       for j in range(1, self.v)]

    def generate_candidates(self):
        self.c_coord = [[r.uniform(1, 1000)
                       for i in range(1, self.c)]
                       for j in range(1, self.c)]


