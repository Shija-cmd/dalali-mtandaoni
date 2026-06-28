from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'phone_number',
        'profile_picture',
        'is_owner',
        'is_seeker',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'DALALI MTANDAONI',
            {
                'fields': (
                    'profile_picture',
                    'phone_number',
                    'is_owner',
                    'is_seeker',
                    'created_at',
                )
            },
        ),
    )

    readonly_fields = (
        'created_at',
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'DALALI MTANDAONI',
            {
                'fields': (
                    'phone_number',
                    'profile_picture',
                    'is_owner',
                    'is_seeker',
                )
            },
        ),
    )
