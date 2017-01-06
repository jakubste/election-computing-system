import names

from ecs.elections.models import Voter, Candidate, Preference
from ecs.geo.models import Point


class ElectionPaintLoader(object):
    def __init__(self, election, candidates_coordinates, voters_coordinates):
        """
            :type election: ecs.elections.models.Election
        """
        self.election = election
        self.candidates_coordinates = candidates_coordinates
        self.voters_coordinates = voters_coordinates

    def load_elections(self):
        self.load_candidates()
        self.load_voters()
        self.compute_preferences()

    def load_candidates(self):
        i = 0
        candidates = []
        for coordinate in self.candidates_coordinates:
            point = Point.objects.create(x=coordinate['x'], y=coordinate['y'])
            name = names.get_first_name()
            candidates.append(Candidate(
                name=name,
                position=point,
                election=self.election,
                soc_id=i + 1
            ))
        Candidate.objects.bulk_create(candidates)

    def load_voters(self):
        voters = []
        for coordinate in self.voters_coordinates:
            point = Point.objects.create(x=coordinate['x'], y=coordinate['y'])
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
