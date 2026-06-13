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

]