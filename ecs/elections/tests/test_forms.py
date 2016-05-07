from ecs.accounts.factories import UserFactory
from ecs.elections.forms import ElectionForm
from ecs.utils.unittestcases import TestCase


class ElectionFormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_form_saves_user(self):
        form = ElectionForm({
            'name': 'Test namee',
            'committee_size': 2
        },user=self.user)
        election = form.save()
        self.assertEqual(
            election.user,
            self.user
        )
