from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [

    # ======================================================
    #                     PUBLIC PAGES
    # ======================================================

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),

    path(
        'terms/',
        views.terms,
        name='terms'
    ),

    path(
        'privacy/',
        views.privacy,
        name='privacy'
    ),

    path(
        'listing-rules/',
        views.listing_rules,
        name='listing_rules'
    ),

    path(
        'listings/',
        views.listings,
        name='listings'
    ),

    path(
        'listings/<int:pk>/',
        views.listing_detail,
        name='listing_detail'
    ),

    path(
        'listings/<int:pk>/unlock-contact/',
        views.unlock_contact,
        name='unlock_contact'
    ),

    path(
        'owner/<int:owner_id>/',
        views.owner_profile,
        name='owner_profile'
    ),

    path(
        'api/home/',
        views.api_home,
        name='api_home'
    ),

    path(
        'location/districts/',
        views.location_districts,
        name='location_districts'
    ),

    path(
        'location/wards/',
        views.location_wards,
        name='location_wards'
    ),

    path(
        'location/streets/',
        views.location_streets,
        name='location_streets'
    ),


    # ======================================================
    #                  OWNER / USER PAGES
    # ======================================================

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'create-listing/',
        views.create_listing,
        name='create_listing'
    ),

    path(
        'my-listings/',
        views.my_listings,
        name='my_listings'
    ),

    path(
        'my-profile/',
        views.my_profile,
        name='my_profile'
    ),

    path(
        'listings/<int:pk>/upload-image/',
        views.upload_listing_image,
        name='upload_listing_image'
    ),

    path(
        'listings/<int:pk>/submit-payment/',
        views.submit_listing_payment,
        name='submit_listing_payment'
    ),

    path(
        'listings/<int:pk>/feature/',
        views.submit_listing_payment,
        name='feature_listing'
    ),

    path(
        'listings/<int:pk>/edit/',
        views.edit_listing,
        name='edit_listing'
    ),

    path(
        'listings/<int:pk>/delete/',
        views.delete_listing,
        name='delete_listing'
    ),

    path(
        'listings/<int:pk>/availability/<str:status>/',
        views.update_listing_availability,
        name='update_listing_availability'
    ),


    # ======================================================
    #                    FAVORITES
    # ======================================================

    path(
        'favorite/<int:listing_id>/',
        views.toggle_favorite,
        name='toggle_favorite'
    ),

    path(
        'favorites/',
        views.my_favorites,
        name='my_favorites'
    ),

    # ======================================================
    #               LISTING APPROVAL
    # ======================================================

    path(
        'listing-approval-requests/',
        views.listing_approval_requests,
        name='listing_approval_requests'
    ),

    path(
        'featured-listings/manage/',
        views.featured_listing_management,
        name='featured_listing_management'
    ),

    path(
        'payment-confirmation-requests/',
        views.payment_confirmation_requests,
        name='payment_confirmation_requests'
    ),

    path(
        'contact-unlock-payment-requests/',
        views.contact_unlock_payment_requests,
        name='contact_unlock_payment_requests'
    ),

    path(
        'contact-unlock-payment/<int:unlock_id>/approve/',
        views.approve_contact_unlock_payment,
        name='approve_contact_unlock_payment'
    ),

    path(
        'contact-unlock-payment/<int:unlock_id>/reject/',
        views.reject_contact_unlock_payment,
        name='reject_contact_unlock_payment'
    ),

    path(
        'listing/<int:listing_id>/payment/approve/',
        views.approve_listing_payment,
        name='approve_listing_payment'
    ),

    path(
        'listing/<int:listing_id>/payment/reject/',
        views.reject_listing_payment,
        name='reject_listing_payment'
    ),

    path(
        'listing/<int:listing_id>/approve/',
        views.approve_listing,
        name='approve_listing'
    ),

    path(
        'listing/<int:listing_id>/reject/',
        views.reject_listing,
        name='reject_listing'
    ),

    path(
        'listing/<int:listing_id>/featured/toggle/',
        views.toggle_featured_listing,
        name='toggle_featured_listing'
    ),


    # ======================================================
    #                     PUBLIC APIs
    # ======================================================

    path(
        'api/categories/',
        views.api_categories,
        name='api_categories'
    ),

    path(
        'api/regions/',
        views.api_regions,
        name='api_regions'
    ),

    path(
        'api/districts/',
        views.api_districts,
        name='api_districts'
    ),

    path(
        'api/wards/',
        views.api_wards,
        name='api_wards'
    ),

    path(
        'api/streets/',
        views.api_streets,
        name='api_streets'
    ),

    path(
        'api/listings/',
        views.api_listings,
        name='api_listings'
    ),

    path(
        'api/listings/<int:listing_id>/',
        views.api_listing_detail,
        name='api_listing_detail'
    ),

    path(
        'api/listings/<int:listing_id>/unlock-contact/',
        views.api_unlock_contact,
        name='api_unlock_contact'
    ),

    path(
        'api/featured-listings/',
        views.api_featured_listings,
        name='api_featured_listings'
    ),

    path(
        'api/recent-listings/',
        views.api_recent_listings,
        name='api_recent_listings'
    ),

    path(
        'api/search/',
        views.api_search_listings,
        name='api_search_listings'
    ),


    # ======================================================
    #                AUTHENTICATION APIs
    # ======================================================

    path(
        'api/register/',
        views.api_register,
        name='api_register'
    ),

    path(
        'api/login/',
        views.api_login,
        name='api_login'
    ),


    # ======================================================
    #               PROTECTED USER APIs
    # ======================================================

    path(
        'api/create-listing/',
        views.api_create_listing,
        name='api_create_listing'
    ),

    path(
        'api/my-profile/',
        views.api_my_profile,
        name='api_my_profile'
    ),

    path(
        'api/my-listings/',
        views.api_my_listings,
        name='api_my_listings'
    ),

    path(
        'api/my-favorites/',
        views.api_my_favorites,
        name='api_my_favorites'
    ),

    path(
        'api/favorite/<int:listing_id>/',
        views.api_toggle_favorite,
        name='api_toggle_favorite'
    ),

    path(
        'api/listings/<int:listing_id>/edit/',
        views.api_update_listing,
        name='api_edit_listing'
    ),

    path(
        'api/listings/<int:listing_id>/delete/',
        views.api_delete_listing,
        name='api_delete_listing'
    ),

    path(
        'api/listings/<int:listing_id>/availability/',
        views.api_update_listing_availability,
        name='api_update_listing_availability'
    ),

    path(
        'api/listings/<int:listing_id>/upload-image/',
        views.api_upload_listing_image,
        name='api_upload_listing_image'
    ),

    path(
        'api/listings/<int:listing_id>/submit-payment/',
        views.api_submit_listing_payment,
        name='api_submit_listing_payment'
    ),

    path(
        'api/payment-methods/',
        views.api_payment_methods,
        name='api_payment_methods'
    ),

    path(
        'api/logout/',
        views.api_logout,
        name='api_logout'
    ),

    path(
        'api/listings/<int:listing_id>/update/',
        views.api_update_listing,
        name='api_update_listing'
    ),

    path(
        'api/my-profile/update/',
        views.api_update_profile,
        name='api_update_profile'
    ),

    path(
        'api/change-password/',
        views.api_change_password,
        name='api_change_password'
    ),

    path(
        'api/owners/<int:owner_id>/',
        views.api_owner_profile,
        name='api_owner_profile'
    ),

    path(
        'api/dashboard/',
        views.api_dashboard,
        name='api_dashboard'
    ),

    path(
        'api/home/',
        views.api_home,
        name='api_home'
    ),

    # ======================================================
    #                     ADMIN APIs
    # ======================================================
    path(
        'api/admin/statistics/',
        views.api_admin_statistics,
        name='api_admin_statistics'
    ),

    path(
        'api/admin/listing-approval-requests/',
        views.listing_approval_requests,
        name='api_admin_listing_approval_requests'
    ),

    path(
        'api/admin/featured-listings/manage/',
        views.api_admin_featured_listing_management,
        name='api_admin_featured_listing_management'
    ),

    path(
        'api/admin/listings/<int:listing_id>/approve/',
        views.api_admin_approve_listing,
        name='api_admin_approve_listing'
    ),

    path(
        'api/admin/listings/<int:listing_id>/reject/',
        views.api_admin_reject_listing,
        name='api_admin_reject_listing'
    ),

    path(
        'api/admin/listings/<int:listing_id>/featured/toggle/',
        views.api_admin_toggle_featured_listing,
        name='api_admin_toggle_featured_listing'
    ),

    path(
        'api/admin/payment-confirmation-requests/',
        views.api_admin_payment_confirmation_requests,
        name='api_admin_payment_confirmation_requests'
    ),

    path(
        'api/admin/contact-unlock-payment-requests/',
        views.api_admin_contact_unlock_payment_requests,
        name='api_admin_contact_unlock_payment_requests'
    ),

    path(
        'api/admin/listings/<int:listing_id>/payment/approve/',
        views.api_admin_approve_listing_payment,
        name='api_admin_approve_listing_payment'
    ),

    path(
        'api/admin/listings/<int:listing_id>/payment/reject/',
        views.api_admin_reject_listing_payment,
        name='api_admin_reject_listing_payment'
    ),

    path(
        'api/admin/contact-unlock-payments/<int:unlock_id>/approve/',
        views.api_admin_approve_contact_unlock_payment,
        name='api_admin_approve_contact_unlock_payment'
    ),

    path(
        'api/admin/contact-unlock-payments/<int:unlock_id>/reject/',
        views.api_admin_reject_contact_unlock_payment,
        name='api_admin_reject_contact_unlock_payment'
    ),

    path(
        'api/listing-status/',
        views.api_listing_status,
        name='api_listing_status'
    ),
]

if settings.DEBUG or settings.DJANGO_SERVE_MEDIA:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
