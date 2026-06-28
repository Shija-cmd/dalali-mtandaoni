from django import forms
from django.utils import timezone
from .models import (
    ContactUnlock,
    District,
    Listing,
    ListingImage,
    PublishingPaymentMethod,
    Region,
    StreetArea,
    Ward,
)
from .validators import validate_image_upload


class ListingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['region'].queryset = Region.objects.all()
        self.fields['district'].queryset = District.objects.none()
        self.fields['ward'].queryset = Ward.objects.none()
        self.fields['street_area'].queryset = StreetArea.objects.none()

        region_id = self.data.get('region') or getattr(
            self.instance,
            'region_id',
            None
        )

        district_id = self.data.get('district') or getattr(
            self.instance,
            'district_id',
            None
        )

        ward_id = self.data.get('ward') or getattr(
            self.instance,
            'ward_id',
            None
        )

        if region_id:

            self.fields['district'].queryset = District.objects.filter(
                region_id=region_id
            )

        if district_id:

            self.fields['ward'].queryset = Ward.objects.filter(
                district_id=district_id
            )

        if ward_id:

            self.fields['street_area'].queryset = StreetArea.objects.filter(
                ward_id=ward_id
            )

    class Meta:

        model = Listing

        fields = [
            'category',
            'title',
            'description',
            'region',
            'district',
            'ward',
            'street_area',
            'location_description',
            'price',
            'owner_id_document',
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

            'region': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'district': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'ward': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'street_area': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'location_description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Optional nearby landmark or extra description'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter price in TZS'
                }
            ),

            'owner_id_document': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*'
                }
            ),

        }

        labels = {
            'street_area': 'Street/Area',
            'location_description': 'Extra Location Description',
            'owner_id_document': 'Owner ID Document',
        }

    def clean_owner_id_document(self):

        id_document = self.cleaned_data.get(
            'owner_id_document'
        )

        if not id_document and not getattr(
            self.instance,
            'owner_id_document',
            None
        ):

            raise forms.ValidationError(
                'Please upload a photo of your ID before submitting this listing.'
            )

        if id_document:

            validate_image_upload(
                id_document
            )

        return id_document


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

    def clean_image(self):

        image = self.cleaned_data.get(
            'image'
        )

        validate_image_upload(
            image
        )

        return image


class ListingPaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        active_methods = list(
            PublishingPaymentMethod.objects.filter(
                is_active=True
            ).order_by(
                'sort_order',
                'name'
            )
        )

        if active_methods:

            self.fields['payment_method'].choices = [
                (
                    '',
                    'Choose payment method'
                )
            ] + [
                (
                    method.code,
                    method.name
                )
                for method in active_methods
            ]

    class Meta:

        model = Listing

        fields = [
            'featured_package',
            'payment_method',
            'payment_reference',
            'payment_note',
        ]

        widgets = {

            'featured_package': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'payment_method': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'payment_reference': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter transaction ID or payment reference'
                }
            ),

            'payment_note': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Optional note for admin'
                }
            ),

        }

        labels = {
            'featured_package': 'Featured Package',
            'payment_method': 'Payment Method',
            'payment_reference': 'Payment Reference',
            'payment_note': 'Payment Note',
        }

    def clean_featured_package(self):

        featured_package = self.cleaned_data.get(
            'featured_package'
        )

        if not featured_package:

            raise forms.ValidationError(
                'Please choose a featured listing package.'
            )

        return featured_package

    def clean_payment_method(self):

        payment_method = self.cleaned_data.get(
            'payment_method'
        )

        if not payment_method:

            raise forms.ValidationError(
                'Please choose the payment method you used.'
            )

        return payment_method

    def clean_payment_reference(self):

        payment_reference = self.cleaned_data.get(
            'payment_reference',
            ''
        ).strip()

        if not payment_reference:

            raise forms.ValidationError(
                'Please enter your payment reference.'
            )

        return payment_reference


class ManualFeaturedListingForm(forms.Form):

    featured_package = forms.ChoiceField(
        choices=Listing.FEATURED_PACKAGE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm'
            }
        ),
        label='Featured Package'
    )
    featured_until = forms.DateTimeField(
        required=False,
        input_formats=[
            '%Y-%m-%dT%H:%M'
        ],
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control form-control-sm',
                'type': 'datetime-local'
            },
            format='%Y-%m-%dT%H:%M'
        ),
        label='Featured Until'
    )

    def clean_featured_until(self):

        featured_until = self.cleaned_data.get(
            'featured_until'
        )

        if featured_until and featured_until <= timezone.now():

            raise forms.ValidationError(
                'Featured expiry must be in the future.'
            )

        return featured_until


class ContactUnlockPaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        active_methods = list(
            PublishingPaymentMethod.objects.filter(
                is_active=True
            ).order_by(
                'sort_order',
                'name'
            )
        )

        if active_methods:

            self.fields['payment_method'].choices = [
                (
                    '',
                    'Choose payment method'
                )
            ] + [
                (
                    method.code,
                    method.name
                )
                for method in active_methods
            ]

    class Meta:

        model = ContactUnlock

        fields = [
            'payment_method',
            'payment_reference',
            'payment_note',
        ]

        widgets = {
            'payment_method': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'payment_reference': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter transaction ID or payment reference'
                }
            ),
            'payment_note': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Optional note for admin'
                }
            ),
        }

        labels = {
            'payment_method': 'Payment Method',
            'payment_reference': 'Payment Reference',
            'payment_note': 'Payment Note',
        }

    def clean_payment_method(self):

        payment_method = self.cleaned_data.get(
            'payment_method'
        )

        if not payment_method:

            raise forms.ValidationError(
                'Please choose the payment method you used.'
            )

        return payment_method

    def clean_payment_reference(self):

        payment_reference = self.cleaned_data.get(
            'payment_reference',
            ''
        ).strip()

        if not payment_reference:

            raise forms.ValidationError(
                'Please enter your payment reference.'
            )

        return payment_reference


class RejectionReasonForm(forms.Form):

    reason = forms.CharField(
        label='Rejection Reason',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain what the user needs to fix.'
            }
        )
    )

    def clean_reason(self):

        reason = self.cleaned_data.get(
            'reason',
            ''
        ).strip()

        if not reason:

            raise forms.ValidationError(
                'Please enter a rejection reason.'
            )

        return reason
