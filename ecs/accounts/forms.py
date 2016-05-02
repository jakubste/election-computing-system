# coding=utf-8
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    class Errors:
        USER_WITH_EMAIL_DOES_NOT_EXIST = u'No user with such email found'
        USER_WITH_USERNAME_DOESNT_EXIST = u'No user with such username found'
        WRONG_PASSWORD = u'Wrong password'

    username = forms.CharField(max_length=255, label=u'Username')
    password = forms.CharField(max_length=255, widget=forms.PasswordInput, label=u'Password')

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        user = None
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username:
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    cleaned_data['username'] = user.username
                except User.DoesNotExist:
                    self.add_error('username', LoginForm.Errors.USER_WITH_EMAIL_DOES_NOT_EXIST)
            else:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    self.add_error('username', LoginForm.Errors.USER_WITH_USERNAME_DOESNT_EXIST)

            if user and not user.check_password(password):
                self.add_error('password', LoginForm.Errors.WRONG_PASSWORD)

        return cleaned_data


class RegistrationForm(forms.Form):
    class Errors:
        EMAIL_ALREADY_USED = u'User with given email already exists'
        USERNAME_ALREADY_USED = u'User with given username already exists'
        CHARACTER_NOT_ALLOWED = u'Username cannot contain \'@\' symbol'

    email = forms.EmailField(max_length=255, label=u'E-mail')
    username = forms.CharField(max_length=255, label=u'Username')
    password = forms.CharField(max_length=255, min_length=4, widget=forms.PasswordInput, label=u'Password')
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': u'Enter e-mail'})
        self.fields['username'].widget.attrs.update({'placeholder': u'Enter username'})
        self.fields['password'].widget.attrs.update({'placeholder': u'Enter password'})
        self.fields['first_name'].widget.attrs.update({'placeholder': u'Enter first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': u'Enter last name'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(RegistrationForm.Errors.EMAIL_ALREADY_USED)
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.find('@') != -1:
            raise forms.ValidationError(RegistrationForm.Errors.CHARACTER_NOT_ALLOWED)
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(RegistrationForm.Errors.USERNAME_ALREADY_USED)
        return username
