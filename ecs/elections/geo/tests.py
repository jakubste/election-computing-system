from math import sqrt

from ecs.elections.geo.models import Point
from ecs.utils.unittestcases import TestCase


class PointTestCase(TestCase):
    def test_euclidean_norm_1(self):
        a = Point.objects.create(x=0, y=0)
        b = Point.objects.create(x=1, y=1)
        self.assertAlmostEqual(
            sqrt(2),
            a.distance(b)
        )

    def test_euclidean_norm_2(self):
        a = Point.objects.create(x=0, y=0)
        b = Point.objects.create(x=-1, y=-1)
        self.assertAlmostEqual(
            sqrt(2),
            a.distance(b)
        )
