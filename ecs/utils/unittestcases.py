import urllib

from django.core.urlresolvers import reverse
from django.test import TestCase as DjangoTestCase

from ecs import settings
from ecs.accounts.factories import UserFactory


class TestCase(DjangoTestCase):
    url = ''

    def get_url(self):
        return reverse(self.url)

    def get_response(self, url=None, method='get', data={}):
        if url is None:
            url = self.get_url()

        return getattr(self.client, method)(url, data)

    def assertViewRequiresLogin(self, url=None, method='get'):
        if url is None:
            url = self.get_url()
        self.client.logout()
        resp = self.get_response(url, method)
        self.assertRedirects(resp, settings.LOGIN_URL + '?next={url}'.format(url=urllib.quote(url)))

    def assertViewOnlyForStaff(self, url):
        self.client.logout()
        user = self.login(username='User1')
        response = self.client.get(url)
        self.assertRedirects(response, '/admin/login/' + '?next={url}'.format(url=urllib.quote(url)))

    def login(self, **user_kwargs):
        user = UserFactory.create(**user_kwargs)
        user.set_password('secret')
        user.save()
        self.client.login(username=user.username, password='secret')
        return user
