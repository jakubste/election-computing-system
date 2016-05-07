from decimal import Decimal

import mock

from ecs.elections.factories import ElectionFactory, VoterFactory, CandidateFactory, PointCandidateFactory, \
    PointVoterFactory, ResultFactory, PreferenceFactory
from ecs.utils.unittestcases import TestCase

mock.patch.object = mock.patch.object


class ElectionTestCase(TestCase):
    def test_is_set_up_flag(self):
        election = ElectionFactory.create()
        self.assertEqual(election.is_set_up(), False)
        VoterFactory.create(election=election)
        self.assertEqual(election.is_set_up(), False)
        CandidateFactory.create(election=election)
        self.assertEqual(election.is_set_up(), True)

    def test_is_set_generated_flag(self):
        empty_election = ElectionFactory.create()

        file_election = ElectionFactory.create()
        file_cs = CandidateFactory.create_batch(4, election=file_election)
        file_vs = VoterFactory.create_batch(10, election=file_election)

        gauss_election = ElectionFactory.create()
        gauss_cs = PointCandidateFactory.create_batch(4, election=gauss_election)
        gauss_vs = PointVoterFactory.create_batch(10, election=gauss_election)

        self.assertEqual(empty_election.is_generated(), False)
        self.assertEqual(file_election.is_generated(), False)
        self.assertEqual(gauss_election.is_generated(), True)


class ResultTestCase(TestCase):
    def setUp(self):
        self.result = ResultFactory.create()

    def test_get_absolute_url(self):
        response = self.client.get(self.result.get_absolute_url())
        self.assertIn(str(self.result), response.content)


class VoterTestCase(TestCase):
    def setUp(self):
        self.voter = VoterFactory.create(repeats=1)
        self.preferences = PreferenceFactory.create_batch(5, voter=self.voter)

    def get_candidates_by_preference(self, nums):
        candidates = []
        for num in nums:
            for preference in self.preferences:
                if preference.preference == num:
                    candidates.append(preference.candidate)
                    break
        return candidates

    def test_calculate_committee_score(self):
        p = 2
        committee = self.get_candidates_by_preference([1, 2, 3])
        self.assertAlmostEquals(
            self.voter.calculate_committee_score(committee, p, 5),
            Decimal(pow(4 ** p + 3 ** p + 2 ** p, 1.0 / p))
        )
        p = 3
        committee = self.get_candidates_by_preference([3, 4, 5])
        self.assertAlmostEquals(
            self.voter.calculate_committee_score(committee, p, 5),
            Decimal(pow(1 ** p + 2 ** p, 1.0 / p))
        )
        p = 8
        committee = self.get_candidates_by_preference([4, 2, 3])
        self.assertAlmostEquals(
            self.voter.calculate_committee_score(committee, p, 5),
            Decimal(pow(1 ** p + 3 ** p + 2 ** p, 1.0 / p))
        )
        p = 8
        committee = self.get_candidates_by_preference([1])
        self.assertAlmostEquals(
            self.voter.calculate_committee_score(committee, p, 5),
            Decimal(4)
        )
        p = 8
        committee = self.get_candidates_by_preference([5])
        self.assertAlmostEquals(
            self.voter.calculate_committee_score(committee, p, 5),
            Decimal(0)
        )

    @mock.patch('ecs.elections.models.ell_p_norm')
    def test_calculate_committee_score_multiplies_by_repeats(self, mocked_ell_p):
        mocked_ell_p.return_value = 2
        committee = self.get_candidates_by_preference([1, 2, 3])
        self.assertEqual(
            self.voter.calculate_committee_score(committee, 4, 5),
            2
        )
        self.voter.repeats = 2
        self.voter.save()
        self.assertEqual(
            self.voter.calculate_committee_score(committee, 4, 5),
            4
        )
        self.voter.repeats = 100
        self.voter.save()
        self.assertEqual(
            self.voter.calculate_committee_score(committee, 4, 5),
            200
        )
