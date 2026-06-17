from django.urls import path

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
        'owner/<int:owner_id>/',
        views.owner_profile,
        name='owner_profile'
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
        'listings/<int:pk>/edit/',
        views.edit_listing,
        name='edit_listing'
    ),

    path(
        'listings/<int:pk>/delete/',
        views.delete_listing,
        name='delete_listing'
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
    #                  VERIFICATION
    # ======================================================

    path(
        'request-verification/',
        views.request_verification,
        name='request_verification'
    ),

    path(
        'verification-requests/',
        views.verification_requests,
        name='verification_requests'
    ),

    path(
        'verification-request/<int:request_id>/approve/',
        views.approve_verification,
        name='approve_verification'
    ),

    path(
        'verification-request/<int:request_id>/reject/',
        views.reject_verification,
        name='reject_verification'
    ),
    
    path(
        'api/my-verification-requests/',
        views.api_my_verification_requests,
        name='api_my_verification_requests'
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
        'listing/<int:listing_id>/approve/',
        views.approve_listing,
        name='approve_listing'
    ),

    path(
        'listing/<int:listing_id>/reject/',
        views.reject_listing,
        name='reject_listing'
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
        'api/listings/<int:listing_id>/upload-image/',
        views.api_upload_listing_image,
        name='api_upload_listing_image'
    ),
    
    path(
        'api/request-verification/',
        views.api_request_verification,
        name='api_request_verification'
    ),
    
    path(
        'api/verification-status/',
        views.api_verification_status,
        name='api_verification_status'
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
        'api/listing-status/',
        views.api_listing_status,
        name='api_listing_status'
    ),
]