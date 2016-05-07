from decimal import Decimal
from math import sqrt

from ecs.utils.math import ell_p_norm
from ecs.utils.unittestcases import TestCase


class EllPNormTestCase(TestCase):
    def test_ell_p_norm_calculating(self):
        self.assertEqual(
            ell_p_norm([1], 1),
            Decimal(1)
        )
        self.assertAlmostEquals(
            ell_p_norm([1], 2),
            Decimal(1)
        )
        self.assertAlmostEquals(
            ell_p_norm([1, 2, 3], 2),
            Decimal(sqrt(1 + 4 + 9))
        )
        self.assertAlmostEquals(
            ell_p_norm([1, 2, 3], 10000),
            Decimal(3)
        )
