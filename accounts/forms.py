from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = (
            'username',
            'phone_number',
            'is_owner',
            'is_seeker',
            'password1',
            'password2',
        )