from . import views
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

app_name = 'users'

urlpatterns =[
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    ]