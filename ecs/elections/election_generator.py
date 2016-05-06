from random import gauss

import names
from django.db import transaction

from ecs.geo.models import Point
from ecs.elections.models import Candidate, Preference
from ecs.elections.models import Voter


class ElectionGenerator(object):
    election = None
    candidates_mean_x = None
    candidates_mean_y = None
    candidates_sigma = None
    voters_mean_x = None
    voters_mean_y = None
    voters_sigma = None
    candidates_amount = None
    voters_amount = None

    def __init__(
            self, election,
            candidates_amount, voters_amount,
            candidates_mean_x, candidates_mean_y, candidates_sigma,
            voters_mean_x, voters_mean_y, voters_sigma
    ):
        """
        :type election: ecs.elections.models.Election
        """
        self.election = election
        self.candidates_amount = candidates_amount
        self.voters_amount = voters_amount
        self.candidates_mean_x = candidates_mean_x
        self.candidates_mean_y = candidates_mean_y
        self.candidates_sigma = candidates_sigma
        self.voters_mean_x = voters_mean_x
        self.voters_mean_y = voters_mean_y
        self.voters_sigma = voters_sigma

    def generate_elections(self):
        self.generate_candidates()
        self.generate_voters()
        self.compute_preferences()

    def generate_candidates(self):
        for i in range(self.candidates_amount):
            x = int(gauss(self.candidates_mean_x, self.candidates_sigma))
            y = int(gauss(self.candidates_mean_y, self.candidates_sigma))
            point = Point.objects.create(x=x, y=y)
            name = names.get_first_name()
            Candidate.objects.create(
                name=name,
                position=point,
                election=self.election,
                soc_id=i + 1
            )

    def generate_voters(self):
        for i in range(self.voters_amount):
            x = int(gauss(self.voters_mean_x, self.voters_sigma))
            y = int(gauss(self.voters_mean_y, self.voters_sigma))
            point = Point.objects.create(x=x, y=y)
            Voter.objects.create(
                repeats=1,
                position=point,
                election=self.election,
            )

    def compute_preferences(self):
        """
            For each voter arranges candidates in order of euclidean norm distances
        """
        with transaction.atomic():
            for voter in self.election.voters.all():
                voter_preference = sorted(
                    self.election.candidates.all(),
                    key=lambda c: voter.position.distance(c.position)
                )
                for i, candidate in enumerate(voter_preference):
                    Preference.objects.create(
                        candidate=candidate,
                        voter=voter,
                        preference=i+1
                    )
