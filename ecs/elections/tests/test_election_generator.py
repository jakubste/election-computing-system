from itertools import izip

import mock

from ecs.elections.election_generator import ElectionGenerator
from ecs.elections.factories import ElectionFactory
from ecs.elections.models import Preference
from ecs.utils.unittestcases import TestCase

mock.patch.object = mock.patch.object


class ElectionGeneratorTestCase(TestCase):
    def setUp(self):
        self.election = ElectionFactory.create()
        self.candidates_amount = 10
        self.voters_amount = 10
        self.generator = ElectionGenerator(
            self.election,
            self.candidates_amount, self.voters_amount,
            0, 0, 10,
            0, 0, 10
        )

    @mock.patch.object(ElectionGenerator, 'generate_candidates')
    @mock.patch.object(ElectionGenerator, 'generate_voters')
    @mock.patch.object(ElectionGenerator, 'compute_preferences')
    def test_generate_elections(self, mocked_compute, mocked_voters_gen, mocked_cand_gen):
        self.generator.generate_elections()
        mocked_compute.assert_called_once()
        mocked_voters_gen.assert_called_once()
        mocked_cand_gen.assert_called_once()

    def test_generate_voters(self):
        self.generator.generate_voters()
        self.assertEqual(
            self.election.voters.count(),
            self.voters_amount
        )

    def test_generate_candidates(self):
        self.generator.generate_candidates()
        self.assertEqual(
            self.election.candidates.count(),
            self.candidates_amount
        )

    def test_compute_preferences(self):
        self.generator.generate_voters()
        self.generator.generate_candidates()
        self.generator.compute_preferences()
        self.assertEqual(
            Preference.objects.filter(candidate__election=self.election).count(),
            self.candidates_amount * self.voters_amount
        )

    def test_preferences_are_in_good_order(self):
        self.generator.generate_elections()
        for voter in self.election.voters.all():
            preferences = Preference.objects.filter(voter=voter).order_by('preference')
            preferences = [voter.position.distance(preference.candidate.position) for preference in preferences]
            self.assertTrue(sorted(preferences) == preferences)
