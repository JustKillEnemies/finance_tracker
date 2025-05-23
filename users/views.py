from django.shortcuts import render
from django.views.generic import CreateView
from .forms import RegisterUserForm, LoginUserForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordChangeView, LoginView


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')