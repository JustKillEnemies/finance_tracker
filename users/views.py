from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from .forms import RegisterUserForm, LoginUserForm, ProfileUserForm, UserPasswordChangeForm, FeedbackCreateForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordChangeView, LoginView, PasswordChangeDoneView
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from .emails import send_contact_email_message
from .utils import get_client_ip
from .models import Feedback
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class ProfileUser(UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    # success_url = reverse_lazy("users:profile")
    success_url = reverse_lazy("users:password_change_done")


class FeedbackCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackCreateForm
    success_message = "Ваше письмо успешно отправлено администрации сайта"
    template_name = "users/feedback.html"
    extra_context = {'title': "Контактная форма"}
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ip_address = get_client_ip(self.request)
            if self.request.user.is_authenticated:
                feedback.user = self.request.user
            send_contact_email_message(feedback.subject, feedback.email,
                                       feedback.content, feedback.ip_address, feedback.user_id)
        return super().form_valid(form)