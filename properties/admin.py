from django.contrib import admin
from .models import Favorite
from accounts.models import User

from .models import (
    Category,
    Listing,
    ListingImage,
    VerificationRequest
)

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(ListingImage)
admin.site.register(Favorite)


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
