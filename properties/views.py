from django.shortcuts import render, get_object_or_404, redirect
from .forms import ListingForm, ListingImageForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from accounts.models import User
from django.contrib import messages
from .models import Favorite
from django.http import HttpResponseForbidden
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes
)


from .serializers import (
    CategorySerializer,
    ListingSerializer,
    UserRegisterSerializer,
    ListingCreateSerializer,
    UserSerializer
)

from .models import (
    Listing, 
    Category,
    Favorite,
    VerificationRequest,

)


def format_whatsapp_number(phone):

    if phone.startswith('0'):
        return '255' + phone[1:]

    return phone

def home(request):

    featured_listings = Listing.objects.filter(
        is_active=True,
        is_approved=True,
        is_featured=True
    )[:6]

    total_listings = Listing.objects.filter(
        is_active=True,
        is_approved=True
    ).count()

    total_users = User.objects.count()

    total_categories = Category.objects.count()

    verified_owners = User.objects.filter(
        is_verified=True
    ).count()
    
    recent_listings = Listing.objects.filter(
        is_active=True,
        is_approved=True
    ).order_by(
        '-created_at'
    )[:6]

    return render(
        request,
        'properties/home.html',
        {
            'featured_listings': featured_listings,
            'total_listings': total_listings,
            'total_users': total_users,
            'total_categories': total_categories,
            'verified_owners': verified_owners,
            'recent_listings': recent_listings,
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
        
    whatsapp_number = format_whatsapp_number(
        listing.owner.phone_number
    )

    return render(
        request,
        'properties/listing_detail.html',
        {
            'listing': listing,
            'is_favorite': is_favorite,
            'whatsapp_number': whatsapp_number,
            
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

    total_favorites = Favorite.objects.filter(
        user=request.user
    ).count()
    
    pending_verification = VerificationRequest.objects.filter(
        user=request.user,
        status='pending'
    ).exists()

    return render(
        request,
        'properties/dashboard.html',
        {
            'total_listings': total_listings,
            'approved_listings': approved_listings,
            'pending_listings': pending_listings,
            'total_favorites': total_favorites,
            'pending_verification': pending_verification,
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
    
    whatsapp_number = format_whatsapp_number(
        owner.phone_number
)

    return render(
        request,
        'properties/owner_profile.html',
        {
            'owner': owner,
            'listings': listings,
            'listing_count': listings.count(),
            'whatsapp_number': whatsapp_number,
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
    
@login_required
def request_verification(request):

    existing_request = VerificationRequest.objects.filter(
        user=request.user,
        status='pending'
    ).exists()

    if not existing_request:

        VerificationRequest.objects.create(
            user=request.user
        )

        messages.success(
            request,
            'Verification request submitted successfully.'
        )

    else:

        messages.warning(
            request,
            'You already have a pending verification request.'
        )

    return redirect(
        'dashboard'
    ) 
    

@login_required
def my_profile(request):

    return redirect(
        'owner_profile',
        owner_id=request.user.id
    )  
    

@login_required
def verification_requests(request):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    requests = VerificationRequest.objects.filter(
        status='pending'
    )

    return render(
        request,
        'properties/verification_requests.html',
        {
            'requests': requests
        }
    ) 
    
    
@login_required
def approve_verification(request, request_id):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    verification_request = get_object_or_404(
        VerificationRequest,
        id=request_id
    )

    verification_request.status = 'approved'
    verification_request.save()

    verification_request.user.is_verified = True
    verification_request.user.save()
    
    messages.success(
        request,
        'Verification approved successfully.'
    )

    return redirect(
        'verification_requests'
    )
    
    
@login_required
def reject_verification(request, request_id):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    verification_request = get_object_or_404(
        VerificationRequest,
        id=request_id
    )

    verification_request.status = 'rejected'
    verification_request.save()

    verification_request.user.is_verified = False
    verification_request.user.save()
    
    messages.warning(
        request,
        'Verification request rejected.'
    )

    return redirect(
        'verification_requests'
    ) 
    
    
@api_view(['GET'])
def api_categories(request):

    categories = Category.objects.all()

    serializer = CategorySerializer(
        categories,
        many=True
    )

    return Response(
        serializer.data
    )
    
    
@api_view(['GET'])
def api_listings(request):

    listings = Listing.objects.filter(
        is_active=True,
        is_approved=True
    )

    serializer = ListingSerializer(
        listings,
        many=True
    )

    return Response(
        serializer.data
    )
    
    
@api_view(['GET'])
def api_listing_detail(
    request,
    listing_id
    ):

    listing = get_object_or_404(
        Listing,
        id=listing_id,
        is_active=True,
        is_approved=True
    )

    serializer = ListingSerializer(
        listing
    )

    return Response(
        serializer.data
    )
    
    
@api_view(['GET'])
def api_featured_listings(request):

    listings = Listing.objects.filter(
        is_active=True,
        is_approved=True,
        is_featured=True
    )

    serializer = ListingSerializer(
        listings,
        many=True
    )

    return Response(
        serializer.data
    )
    

@api_view(['GET'])
def api_recent_listings(request):

    listings = Listing.objects.filter(
        is_active=True,
        is_approved=True
    ).order_by('-created_at')[:10]

    serializer = ListingSerializer(
        listings,
        many=True
    )

    return Response(
        serializer.data
    )
    
    
@api_view(['GET'])
def api_search_listings(request):

    query = request.GET.get(
        'q',
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

    serializer = ListingSerializer(
        listings,
        many=True
    )

    return Response(
        serializer.data
    )
    
    
@api_view(['POST'])
def api_register(request):

    serializer = UserRegisterSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                'message': 'Account created successfully.'
            },
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )
    
    
@api_view(['POST'])
def api_login(request):

    username = request.data.get(
        'username'
    )

    password = request.data.get(
        'password'
    )

    user = authenticate(
        username=username,
        password=password
    )

    if user:

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                'token': token.key,
                'username': user.username,
                'user_id': user.id,
            }
        )

    return Response(
        {
            'error': 'Invalid credentials'
        },
        status=400
    )
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_listing(request):

    serializer = ListingCreateSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(
            owner=request.user
        )

        return Response(
            serializer.data,
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_profile(request):

    serializer = UserSerializer(
        request.user
    )

    return Response(
        serializer.data
    )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_listings(request):

    listings = Listing.objects.filter(
        owner=request.user
    )

    serializer = ListingSerializer(
        listings,
        many=True
    )

    return Response(
        serializer.data
    )