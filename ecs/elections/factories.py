import random

import factory

from ecs.accounts.factories import UserFactory
from ecs.elections.models import Election


class ElectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Election

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: "Election_%03d" % n)
    committee_size = factory.lazy_attribute(lambda i: random.randint(1, 50))
