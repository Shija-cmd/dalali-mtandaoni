from django import forms
from .models import Listing, ListingImage


class ListingForm(forms.ModelForm):

    class Meta:

        model = Listing

        fields = [
            'category',
            'title',
            'description',
            'location',
            'latitude',
            'longitude',
            'price',
        ]

        widgets = {

            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Modern 3 Bedroom House'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Describe your property...'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Mbeya, Tanzania'
                }
            ),

            'latitude': forms.HiddenInput(),

            'longitude': forms.HiddenInput(),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter price in TZS'
                }
            ),

        }


class ListingImageForm(forms.ModelForm):

    class Meta:

        model = ListingImage

        fields = [
            'image'
        ]

        widgets = {

            'image': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            )

        }