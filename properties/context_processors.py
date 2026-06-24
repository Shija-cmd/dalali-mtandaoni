from .models import (
    VerificationRequest,
    Listing,
)


def verification_status(request):

    pending_verification = False
    pending_verification_request = None
    pending_user_requests = 0
    pending_listing_requests = 0

    if request.user.is_authenticated:

        pending_verification_request = VerificationRequest.objects.filter(
            user=request.user,
            status='pending'
        ).first()

        pending_verification = pending_verification_request is not None

        if request.user.is_superuser:

            pending_user_requests = VerificationRequest.objects.filter(
                status='pending'
            ).count()

            pending_listing_requests = Listing.objects.filter(
                is_approved=False
            ).count()

    return {

        'pending_verification': pending_verification,

        'pending_verification_request': pending_verification_request,

        'pending_user_requests': pending_user_requests,

        'pending_listing_requests': pending_listing_requests,

    }
