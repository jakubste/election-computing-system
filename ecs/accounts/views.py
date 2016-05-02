from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.debug import sensitive_variables
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from ecs.accounts.forms import LoginForm, RegistrationForm


class Home(TemplateView):
    template_name = 'home.html'


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = 'accounts:home'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user.is_authenticated:
            login(self.request, user)
        return redirect(self.success_url)


def logout_view(request):
    logout(request)
    return redirect('accounts:home')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = 'accounts:home'

    @sensitive_variables('password')
    def form_valid(self, form):
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)
