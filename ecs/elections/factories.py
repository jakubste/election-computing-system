import random

import factory

from ecs.accounts.factories import UserFactory
from ecs.elections.models import Election, Candidate, Voter, Preference


class ElectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Election

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: "Election_%03d" % n)
    committee_size = factory.lazy_attribute(lambda i: random.randint(1, 50))


class CandidateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Candidate

    name = factory.Sequence(lambda n: "Candidate_%03d" % n)
    election = factory.SubFactory(ElectionFactory)


class VoterFactory(factory.DjangoModelFactory):
    class Meta:
        model = Voter

    repeats = factory.lazy_attribute(lambda i: random.randint(1, 5))
    election = factory.SubFactory(ElectionFactory)


class PreferenceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Preference

    candidate = factory.SubFactory(CandidateFactory)
    voter = factory.SubFactory(VoterFactory)

    @factory.lazy_attribute
    def preference(self):
        preferences = Preference.objects.filter(voter=self.voter).values_list('preference', flat=True)
        if preferences:
            return max(preferences) + 1
        else:
            return 1
