from random import gauss

import names

from ecs.elections.models import Candidate, Preference
from ecs.elections.models import Voter
from ecs.geo.models import Point


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
        candidates = []
        for i in range(self.candidates_amount):
            x = int(gauss(self.candidates_mean_x, self.candidates_sigma))
            y = int(gauss(self.candidates_mean_y, self.candidates_sigma))
            point = Point.objects.create(x=x, y=y)
            name = names.get_first_name()
            candidates.append(Candidate(
                name=name,
                position=point,
                election=self.election,
                soc_id=i + 1
            ))
        Candidate.objects.bulk_create(candidates)

    def generate_voters(self):
        voters = []
        for i in range(self.voters_amount):
            x = int(gauss(self.voters_mean_x, self.voters_sigma))
            y = int(gauss(self.voters_mean_y, self.voters_sigma))
            point = Point.objects.create(x=x, y=y)
            voters.append(Voter(
                repeats=1,
                position=point,
                election=self.election,
            ))
        Voter.objects.bulk_create(voters)

    def compute_preferences(self):
        """
            For each voter arranges candidates in order of euclidean norm distances
        """
        voters = self.election.voters.all().select_related('position')
        candidates = self.election.candidates.all().select_related('position')
        preferences = []
        for voter in voters:
            voter_preference = sorted(
                candidates,
                key=lambda c: voter.position.distance(c.position)
            )
            for i, candidate in enumerate(voter_preference):
                preferences.append(Preference(
                    candidate=candidate,
                    voter=voter,
                    preference=i + 1
                ))
        Preference.objects.bulk_create(preferences)
