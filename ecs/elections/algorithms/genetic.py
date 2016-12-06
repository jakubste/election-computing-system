from random import sample, randint

from datetime import datetime, timedelta

from ecs.elections.algorithms.algorithm import Algorithm
from ecs.elections.algorithms.helpers import binom


class Individual(object):
    committee = None
    score = 0
    algorithm = None

    def __init__(self, committee, algorithm):
        self.committee = committee
        self.algorithm = algorithm
        time_a = datetime.now()
        self.score = self.algorithm.calculate_committee_score_from_prefetched(committee)
        time_b = datetime.now()
        algorithm.diff += time_b - time_a

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
        self.fetch_preferences()
        self.diff = timedelta()

        count = binom(
            self.election.candidates.count(),
            self.election.committee_size
        )

        pks = self.election.candidates.values_list('pk', flat=True)
        combinations = []
        while len(combinations) < count:
            committee = sample(pks, self.election.committee_size)
            if committee not in combinations:
                combinations.append(committee)

        pool = [self.election.candidates.filter(pk__in=pk_list) for pk_list in combinations]
        pool = [Individual(c, self) for c in pool]

        for i in xrange(50):
            print 'cycle', i, 'from 50'
            ma = sample(pool, count/2)
            mb = sample(pool, count/2)
            for a,b in zip(ma, mb):
                pool.append(a.cross(b))
            for ind in pool:
                new_ind = ind.mutate()
                if new_ind:
                    pool.append(new_ind)
            pool = sorted(pool, key=lambda x: x.score, reverse=True)
            pool = pool[:count]
            print pool[0].score
        print self.diff

        return pool[0].committee