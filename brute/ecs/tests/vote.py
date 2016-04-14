from decimal import Decimal
from math import sqrt
from unittest import TestCase

import mock

from ecs.vote import Vote


class VoteTest(TestCase):
    def test_ell_p_norm_calculating(self):
        self.assertEqual(
            Vote.ell_p_norm([1], 1),
            Decimal(1)
        )
        self.assertAlmostEquals(
            Vote.ell_p_norm([1], 2),
            Decimal(1)
        )
        self.assertAlmostEquals(
            Vote.ell_p_norm([1, 2, 3], 2),
            Decimal(sqrt(1 + 4 + 9))
        )
        self.assertAlmostEquals(
            Vote.ell_p_norm([1, 2, 3], 10000),
            Decimal(3)
        )

    def test_calculate_committee_score(self):
        vote = Vote(1, [1, 2, 3, 4, 5])
        p = 2
        committee = [1, 2, 3]
        self.assertAlmostEquals(
            vote.calculate_committee_score(committee, p),
            Decimal(pow(4 ** p + 3 ** p + 2 ** p, 1.0 / p))
        )
        p = 3
        committee = [5, 4, 3]
        self.assertAlmostEquals(
            vote.calculate_committee_score(committee, p),
            Decimal(pow(1 ** p + 2 ** p, 1.0 / p))
        )
        p = 8
        committee = [4, 2, 3]
        self.assertAlmostEquals(
            vote.calculate_committee_score(committee, p),
            Decimal(pow(1 ** p + 3 ** p + 2 ** p, 1.0 / p))
        )
        p = 8
        committee = [1]
        self.assertAlmostEquals(
            vote.calculate_committee_score(committee, p),
            Decimal(4)
        )
        p = 8
        committee = [5]
        self.assertAlmostEquals(
            vote.calculate_committee_score(committee, p),
            Decimal(0)
        )

    @mock.patch.object(Vote, 'ell_p_norm')
    def test_calculate_committee_score_multiplies_by_repeats(self, mocked_ell_p):
        mocked_ell_p.return_value = 2
        vote = Vote(1, [1, 2, 3, 4, 5])
        self.assertEqual(
            vote.calculate_committee_score([1, 2, 3], 4),
            2
        )
        vote.repeats = 2
        self.assertEqual(
            vote.calculate_committee_score([1, 2, 3], 4),
            4
        )
        vote.repeats = 100
        self.assertEqual(
            vote.calculate_committee_score([1, 2, 3], 4),
            200
        )
