from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'password1',
            'password2',
        )
        
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        for field in self.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })


class UserProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
        )

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'profile_picture': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*'
                }
            ),

        }
