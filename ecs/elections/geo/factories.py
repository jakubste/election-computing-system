import random

import factory

from ecs.elections.geo.models import Point


class PointFactory(factory.DjangoModelFactory):
    class Meta:
        model = Point

    x = factory.lazy_attribute(lambda i: random.randint(0, 1000))
    y = factory.lazy_attribute(lambda i: random.randint(0, 1000))

