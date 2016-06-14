from random import shuffle, sample, randint

from ecs.elections.algorithms.algorithm import Algorithm


class Individual(object):
    committee = None
    score = 0
    algorithm = None

    def __init__(self, committee, algorithm):
        self.committee = committee
        self.algorithm = algorithm
        self.score = self.algorithm.calculate_committee_score_from_prefetched(committee)

    def cross(self, other):
        new_committee = []
        self_committee = sample(self.committee, len(self.committee))
        other_committee = sample(other.committee, len(other.committee))
        for a, b in zip(self_committee, other_committee):
            if a not in new_committee:
                new_committee.append(a)
            if b not in new_committee:
                new_committee.append(b)
        new_committee = new_committee[:self.algorithm.election.committee_size]
        new_committee = sorted(new_committee)
        return Individual(committee=new_committee, algorithm=self.algorithm)

    def mutate(self):
        if randint(0, 100) > 10:
            return None
        candidates = list(self.algorithm.election.candidates.all())
        new_candidate = None
        new_committee = list(self.committee)
        while True:
            new_candidate = sample(candidates, 1)[0]
            if new_candidate not in self.committee:
                break
        new_committee.remove(sample(self.committee, 1)[0])
        new_committee.append(new_candidate)
        return Individual(committee=new_committee, algorithm=self.algorithm)


class GeneticAlgorithm(Algorithm):
    preferences = None

    def run(self):
        combinations = list(self.get_committee_combinations())
        self.fetch_preferences()

        count = 50
        pool = sample(combinations, len(combinations))[:count]
        pool = [Individual(c, self) for c in pool]

        for i in xrange(50):
            print 'cycle', i, 'from 50'
            ma = sample(pool, count/2)
            mb = sample(pool, count/2)
            for a,b in zip(ma, mb):
                pool.append(a.cross(b))
            new = []
            for ind in pool:
                new_ind = ind.mutate()
                if new_ind:
                    new.append(new_ind)
            pool = pool + new
            pool = sorted(pool, key=lambda x: x.score, reverse=True)
            pool = pool[:count]
            print pool[0].score

        return pool[0].committee
