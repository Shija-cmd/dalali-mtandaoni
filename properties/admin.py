from django.contrib import admin
from .models import Favorite
from accounts.models import User

from .models import (
    Category,
    ContactUnlock,
    Listing,
    ListingImage,
    PublishingPaymentMethod,
    Region,
    District,
    Ward,
    StreetArea,
    VerificationRequest
)

admin.site.register(Category)
admin.site.register(ListingImage)
admin.site.register(Favorite)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):

    search_fields = (
        'name',
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'region',
    )

    list_filter = (
        'region',
    )

    search_fields = (
        'name',
        'region__name',
    )


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'district',
    )

    list_filter = (
        'district__region',
        'district',
    )

    search_fields = (
        'name',
        'district__name',
    )


@admin.register(StreetArea)
class StreetAreaAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'ward',
    )

    list_filter = (
        'ward__district__region',
        'ward__district',
        'ward',
    )

    search_fields = (
        'name',
        'ward__name',
    )


@admin.register(ContactUnlock)
class ContactUnlockAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'listing',
        'amount',
        'payment_status',
        'payment_method',
        'payment_reference',
        'is_paid',
        'unlocked_at',
        'expires_at',
        'created_at',
    )

    list_filter = (
        'payment_status',
        'payment_method',
        'is_paid',
        'created_at',
        'expires_at',
    )

    search_fields = (
        'user__username',
        'listing__title',
        'payment_reference',
    )


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'owner',
        'payment_status',
        'featured_package',
        'featured_until',
        'payment_method',
        'payment_reference',
        'availability_status',
        'region',
        'district',
        'ward',
        'street_area',
        'owner_id_document',
        'is_approved',
        'is_featured',
        'is_active',
        'created_at',
    )

    list_filter = (
        'payment_status',
        'featured_package',
        'payment_method',
        'availability_status',
        'region',
        'district',
        'ward',
        'street_area',
        'is_approved',
        'is_featured',
        'is_active',
    )

    search_fields = (
        'title',
        'owner__username',
        'owner__phone_number',
        'payment_reference',
    )


@admin.register(PublishingPaymentMethod)
class PublishingPaymentMethodAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'code',
        'lipa_number',
        'is_active',
        'sort_order',
        'updated_at',
    )

    list_filter = (
        'is_active',
        'code',
    )

    search_fields = (
        'name',
        'code',
        'lipa_number',
    )

    ordering = (
        'sort_order',
        'name',
    )


@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'status',
        'id_document',
        'created_at',
    )

    list_filter = (
        'status',
    )

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        super().save_model(
            request,
            obj,
            form,
            change
        )

        if obj.status == 'approved':

            obj.user.is_verified = True
            obj.user.save()

        elif obj.status == 'rejected':

            obj.user.is_verified = False
            obj.user.save()
