from django.contrib.auth import login
from django.core.urlresolvers import reverse

from ecs.accounts.factories import UserFactory
from ecs.elections.factories import ElectionFactory
from ecs.utils.unittestcases import TestCase


class ElectionListTestCase(TestCase):
    def setUp(self):
        self.url = 'elections:election_list'

    def test_login_required(self):
        self.assertViewRequiresLogin()

    def test_list_own_elections(self):
        ElectionFactory.create()
        user = self.login()
        ElectionFactory.create(user=user)
        response = self.client.get(self.get_url())
        self.assertEqual(
            len(response.context['elections']),
            1
        )
