from decimal import Decimal
from math import sqrt
from unittest import TestCase

import mock

from ecs.voter import Voter
from ecs.candidate import Candidate


class VoteTest(TestCase):

    candidates = [
        Candidate(1, "Monika"),
        Candidate(2, "Weronika"),
        Candidate(3, "Beata"),
        Candidate(4, "Zuzanna"),
        Candidate(5, "Alicja")
    ]

    def test_ell_p_norm_calculating(self):
        self.assertEqual(
            Voter.ell_p_norm([1], 1),
            Decimal(1)
        )
        self.assertAlmostEquals(
            Voter.ell_p_norm([1], 2),
            Decimal(1)
        )
        self.assertAlmostEquals(
            Voter.ell_p_norm([1, 2, 3], 2),
            Decimal(sqrt(1 + 4 + 9))
        )
        self.assertAlmostEquals(
            Voter.ell_p_norm([1, 2, 3], 10000),
            Decimal(3)
        )

    def test_calculate_committee_score(self):
        vote = Voter(1, Voter.int_list_or_tuple_to_candidate_list_or_tuple(self.candidates, [1, 2, 3, 4, 5]))
        p = 2
        committee = Voter.int_list_or_tuple_to_candidate_list_or_tuple(self.candidates, [1, 2, 3])
        self.assertAlmostEquals(
            vote.calculate_committee_score(committee, p),
            Decimal(pow(4 ** p + 3 ** p + 2 ** p, 1.0 / p))
        )
        p = 3
        committee = Voter.int_list_or_tuple_to_candidate_list_or_tuple(self.candidates, [5, 4, 3])
        self.assertAlmostEquals(
            vote.calculate_committee_score(committee, p),
            Decimal(pow(1 ** p + 2 ** p, 1.0 / p))
        )
        p = 8
        committee = Voter.int_list_or_tuple_to_candidate_list_or_tuple(self.candidates, [4, 2, 3])
        self.assertAlmostEquals(
            vote.calculate_committee_score(committee, p),
            Decimal(pow(1 ** p + 3 ** p + 2 ** p, 1.0 / p))
        )
        p = 8
        committee = Voter.int_list_or_tuple_to_candidate_list_or_tuple(self.candidates, [1])
        self.assertAlmostEquals(
            vote.calculate_committee_score(committee, p),
            Decimal(4)
        )
        p = 8
        committee = Voter.int_list_or_tuple_to_candidate_list_or_tuple(self.candidates, [5])
        self.assertAlmostEquals(
            vote.calculate_committee_score(committee, p),
            Decimal(0)
        )

    @mock.patch.object(Voter, 'ell_p_norm')
    def test_calculate_committee_score_multiplies_by_repeats(self, mocked_ell_p):
        mocked_ell_p.return_value = 2
        vote = Voter(1, Voter.int_list_or_tuple_to_candidate_list_or_tuple(self.candidates, [1, 2, 3, 4, 5]))
        self.assertEqual(
            vote.calculate_committee_score(Voter.int_list_or_tuple_to_candidate_list_or_tuple(self.candidates, [1, 2, 3]), 4),
            2
        )
        vote.repeats = 2
        self.assertEqual(
            vote.calculate_committee_score(Voter.int_list_or_tuple_to_candidate_list_or_tuple(self.candidates, [1, 2, 3]), 4),
            4
        )
        vote.repeats = 100
        self.assertEqual(
            vote.calculate_committee_score(Voter.int_list_or_tuple_to_candidate_list_or_tuple(self.candidates, [1, 2, 3]), 4),
            200
        )
