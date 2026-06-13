from django.shortcuts import render, get_object_or_404, redirect
from .forms import ListingForm, ListingImageForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from accounts.models import User
from django.contrib import messages

from .models import (
    Listing, 
    Category,
    Favorite,

)




def home(request):

    featured_listings = Listing.objects.filter(
        is_active=True,
        is_approved=True,
        is_featured=True
    )[:6]

    return render(
        request,
        'properties/home.html',
        {
            'featured_listings': featured_listings
        }
    )
    
def about(request):

    return render(
        request,
        'properties/about.html'
    ) 
    
def contact(request):

    return render(
        request,
        'properties/contact.html'
    ) 
    

def listings(request):

    query = request.GET.get(
        'q',
        ''
    )

    category_id = request.GET.get(
        'category',
        ''
    )
    
    min_price = request.GET.get(
        'min_price',
        ''
    )

    max_price = request.GET.get(
        'max_price',
        ''
    )

    listings = Listing.objects.filter(
        is_active=True,
        is_approved=True
    )

    if query:

        listings = listings.filter(

            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)

        )

    if category_id:

        listings = listings.filter(
            category_id=category_id
        )
        
    if min_price:

        listings = listings.filter(
            price__gte=min_price
        )

    if max_price:

        listings = listings.filter(
            price__lte=max_price
        )    

    categories = Category.objects.all()
    
    paginator = Paginator(
        listings,
        15
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
    request,
        'properties/listings.html',
        {
            'listings': page_obj,
            'page_obj': page_obj,
            'categories': categories,
            'query': query,
            'selected_category': category_id,
            'min_price': min_price,
            'max_price': max_price,
        }
    ) 

def listing_detail(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk,
        is_active=True
    )
    
    is_favorite = False

    if request.user.is_authenticated:

        is_favorite = Favorite.objects.filter(
            user=request.user,
            listing=listing
        ).exists()

    return render(
        request,
        'properties/listing_detail.html',
        {
            'listing': listing,
            'is_favorite': is_favorite,
        }
    )
    
@login_required
def create_listing(request):

    if request.method == 'POST':

        form = ListingForm(request.POST)

        if form.is_valid():

            listing = form.save(commit=False)

            listing.owner = request.user

            listing.save()
            
            messages.success(
                request,
                'Listing created successfully.'
            )

            return redirect(
                'listing_detail',
                pk=listing.pk
            )

    else:

        form = ListingForm()

    return render(
        request,
        'properties/create_listing.html',
        {
            'form': form
        }
    ) 
    
@login_required
def upload_listing_image(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        form = ListingImageForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            image = form.save(commit=False)

            image.listing = listing

            image.save()

            return redirect(
                'listing_detail',
                pk=listing.pk
            )

    else:

        form = ListingImageForm()

    return render(
        request,
        'properties/upload_image.html',
        {
            'form': form,
            'listing': listing
        }
    ) 
    
@login_required
def my_listings(request):

    listings = Listing.objects.filter(
        owner=request.user
    )

    return render(
        request,
        'properties/my_listings.html',
        {
            'listings': listings
        }
    )
    
@login_required
def edit_listing(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        form = ListingForm(
            request.POST,
            instance=listing
        )

        if form.is_valid():

            form.save()
            
            messages.success(
                request,
                'Listing updated successfully.'
            )

            return redirect(
                'listing_detail',
                pk=listing.pk
            )

    else:

        form = ListingForm(
            instance=listing
        )

    return render(
        request,
        'properties/edit_listing.html',
        {
            'form': form,
            'listing': listing
        }
    )  
    
@login_required
def delete_listing(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        listing.delete()
        
        messages.success(
            request,
            'Listing deleted successfully.'
        )

        return redirect('my_listings')

    return render(
        request,
        'properties/delete_listing.html',
        {
            'listing': listing
        }
    )
    
@login_required
def dashboard(request):

    listings = Listing.objects.filter(
        owner=request.user
    )

    total_listings = listings.count()

    approved_listings = listings.filter(
        is_approved=True
    ).count()

    pending_listings = listings.filter(
        is_approved=False
    ).count()

    return render(
        request,
        'properties/dashboard.html',
        {
            'total_listings': total_listings,
            'approved_listings': approved_listings,
            'pending_listings': pending_listings,
        }
    ) 
    
def owner_profile(request, owner_id):

    owner = get_object_or_404(
        User,
        id=owner_id
    )

    listings = Listing.objects.filter(
        owner=owner,
        is_active=True,
        is_approved=True
    )

    return render(
        request,
        'properties/owner_profile.html',
        {
            'owner': owner,
            'listings': listings,
        }
    ) 
    
@login_required
def toggle_favorite(request, listing_id):

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    favorite = Favorite.objects.filter(
        user=request.user,
        listing=listing
    )

    if favorite.exists():

        favorite.delete()

        messages.info(
            request,
            'Listing removed from favorites.'
        )

    else:

        Favorite.objects.create(
            user=request.user,
            listing=listing
        )

        messages.success(
            request,
            'Listing added to favorites.'
        )

    return redirect(
        'listing_detail',
        pk=listing.id
    )  
    
@login_required
def my_favorites(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related(
        'listing'
    )

    return render(
        request,
        'properties/my_favorites.html',
        {
            'favorites': favorites
        }
    )       