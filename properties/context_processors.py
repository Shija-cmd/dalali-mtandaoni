from django.conf import settings

from .models import ContactUnlock, Listing


def verification_status(request):

    pending_listing_requests = 0
    pending_featured_payment_requests = 0
    pending_contact_unlock_requests = 0
    pending_payment_requests = 0

    if request.user.is_authenticated:

        if request.user.is_superuser:

            pending_listing_requests = Listing.objects.filter(
                is_approved=False
            ).count()

            pending_featured_payment_requests = Listing.objects.filter(
                payment_status='pending'
            ).count()

            pending_contact_unlock_requests = ContactUnlock.objects.filter(
                payment_status='pending'
            ).count()

            pending_payment_requests = (
                pending_featured_payment_requests
                + pending_contact_unlock_requests
            )

    return {
        'APP_VERSION': settings.APP_VERSION,
        'pending_listing_requests': pending_listing_requests,
        'pending_featured_payment_requests': pending_featured_payment_requests,
        'pending_contact_unlock_requests': pending_contact_unlock_requests,
        'pending_payment_requests': pending_payment_requests,
    }
