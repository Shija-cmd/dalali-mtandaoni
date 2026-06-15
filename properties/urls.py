from django.urls import path

from . import views


urlpatterns = [

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
        'create-listing/',
        views.create_listing,
        name='create_listing'
    ),
    
    path(
        'listings/<int:pk>/upload-image/',
        views.upload_listing_image,
        name='upload_listing_image'
    ),
    
    path(
        'my-listings/',
        views.my_listings,
        name='my_listings'
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
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),
    
    path(
        'owner/<int:owner_id>/',
        views.owner_profile,
        name='owner_profile'
    ),
    
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
    
    path(
        'request-verification/',
        views.request_verification,
        name='request_verification'
    ),
    
    path(
        'my-profile/',
        views.my_profile,
        name='my_profile'
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
]