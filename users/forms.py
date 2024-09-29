from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, UserChangeForm

from mailing_service.forms import StyleFormMixin
from users.models import User


class UserRegistrationForm(StyleFormMixin,UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')