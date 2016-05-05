from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from ecs.utils.unittestcases import TestCase


class RegisterViewTest(TestCase):
    url = 'accounts:register'

    def setUp(self):
        self.data = {
            'username': 'Moniczka86',
            'email': 'test@example.com',
            'password': 'haslo123',
        }

    def test_creates_user(self):
        response = self.get_response(method='post', data=self.data)
        self.assertEquals(302, response.status_code)
        user = User.objects.get(username=self.data['username'])
        self.assertEquals(response.wsgi_request.user, user)

    def test_does_not_create_user(self):
        data = self.data.copy()
        data['email'] = ""

        response = self.get_response(method='post', data=data)

        self.assertEquals(200, response.status_code)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(
            User.objects.filter(username=self.data['username']).exists()
        )

    def test_does_not_create_user_with_same_email(self):
        response = self.get_response(method='post', data=self.data)
        self.assertEquals(302, response.status_code)

        data = self.data.copy()
        data['username'] = "other_username"

        response = self.get_response(method='post', data=data)
        self.assertEquals(200, response.status_code)
        self.assertTrue(response.context['form'].errors)

    def test_does_not_create_user_with_same_username(self):
        response = self.get_response(method='post', data=self.data)
        self.assertEquals(302, response.status_code)

        data = self.data.copy()
        data['email'] = "other@email.com"

        response = self.get_response(method='post', data=data)
        self.assertEquals(200, response.status_code)
        self.assertTrue(response.context['form'].errors)

    def test_does_not_create_user_with_username_like_email(self):
        response = self.get_response(method='post', data=self.data)
        self.assertEquals(302, response.status_code)

        data = self.data.copy()
        data['username'] = "cant_have@in_email.com"

        response = self.get_response(method='post', data=data)
        self.assertEquals(200, response.status_code)
        self.assertTrue(response.context['form'].errors)

    def test_already_exists(self):
        data = self.data.copy()
        self.get_response(method='post', data=data)
        data['email'] = 'test+moniczka@example.com'
        response = self.get_response(method='post', data=data)

        self.assertEquals(200, response.status_code)
        self.assertTrue(response.context['form'].errors)
        self.assertEquals(
            User.objects.get(username=self.data['username']).email,
            self.data['email']
        )

    def test_passes_form(self):
        response = self.get_response()

        self.assertEquals(200, response.status_code)
        self.assertIn('form', response.context)


class LoginTestView(TestCase):
    def setUp(self):
        self.url = reverse('accounts:login')
        self.home_url = reverse('accounts:home')
        self.username = 'henio'
        self.email = 'henio@wp.pl'
        self.password = 'abc123'
        User.objects.filter(username=self.username).delete()
        User.objects.create_user(self.username, self.email, self.password)

    def test_logs_user_by_username(self):
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEquals(302, response.status_code)
        response = self.client.get(self.home_url)
        self.assertTrue(response.context['user'].is_authenticated())

    def test_logs_user_by_email(self):
        response = self.client.post(self.url, {'username': self.email, 'password': self.password})
        self.assertEquals(302, response.status_code)
        response = self.client.get(self.home_url)
        self.assertTrue(response.context['user'].is_authenticated())

    def test_wrong_username(self):
        response = self.client.post(self.url, {'username': 'bad_username', 'password': self.password})
        self.assertEquals(200, response.status_code)
        self.assertIn('username', response.context['form'].errors)

    def test_wrong_email(self):
        response = self.client.post(self.url, {'username': 'bad@mail.com', 'password': self.password})
        self.assertEquals(200, response.status_code)
        self.assertIn('username', response.context['form'].errors)

    def test_wrong_password(self):
        response = self.client.post(self.url, {'username': self.username, 'password': 'i_dont_know'})
        self.assertEquals(200, response.status_code)
        self.assertIn('password', response.context['form'].errors)


class LogoutView(TestCase):
    def setUp(self):
        self.user = self.login(username='LogoutTestUser')
        self.url = reverse('accounts:logout')

    def test_logout_logouts_user(self):
        self.client.get(self.url)
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.context['user'].is_authenticated(), False)
