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
from .pagination import ListingPagination
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import (
    api_view,
    permission_classes
)


from .serializers import (
    CategorySerializer,
    ListingSerializer,
    UserRegisterSerializer,
    ListingCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
    ListingImageCreateSerializer,
    VerificationRequestSerializer,
)

from .models import (
    Listing, 
    Category,
    Favorite,
    VerificationRequest,

)

# ==========================================================
#                     HELPER FUNCTIONS
# ==========================================================
def format_whatsapp_number(phone):

    if phone.startswith('0'):
        return '255' + phone[1:]

    return phone

# ==========================================================
#                     PUBLIC VIEWS
# ==========================================================
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
    
    sort = request.GET.get(
        'sort',
        'newest'
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
        
    # Sorting

    if sort == "price_low":

        listings = listings.order_by("price")

    elif sort == "price_high":

        listings = listings.order_by("-price")

    elif sort == "oldest":

        listings = listings.order_by("created_at")

    else:

        listings = listings.order_by("-created_at")    

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
            'sort': sort,
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
    
    related_listings = Listing.objects.filter(
        category=listing.category,
        is_active=True,
        is_approved=True
    ).exclude(
        id=listing.id
    )[:3]

    return render(
        request,
        'properties/listing_detail.html',
        {
            'listing': listing,
            'is_favorite': is_favorite,
            'whatsapp_number': whatsapp_number,
            'related_listings': related_listings,
            
        }
    )
    
@login_required
def create_listing(request):

    if not request.user.is_verified:

        messages.warning(
            request,
            'Your account must be verified before creating listings; please request verification'
        )

        return redirect(
            'dashboard'
        )

    if request.method == 'POST':

        form = ListingForm(
            request.POST
        )

        if form.is_valid():

            listing = form.save(
                commit=False
            )

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


# ==========================================================
#                  OWNER / USER VIEWS
# ==========================================================    
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
    
    return render(
        request,
        'properties/dashboard.html',
        {
            'total_listings': total_listings,
            'approved_listings': approved_listings,
            'pending_listings': pending_listings,
            'total_favorites': total_favorites,
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


# ==========================================================
#                  FAVORITES VIEWS
# ==========================================================    
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


# ==========================================================
#                VERIFICATION VIEWS
# ==========================================================    
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
    ).select_related(
        'user'
    )
    
    for verification_request in requests:

        user = verification_request.user

        user.total_listings = user.listing_set.count()

        user.approved_listings = user.listing_set.filter(
            is_approved=True
        ).count()

        user.pending_listings = user.listing_set.filter(
            is_approved=False
        ).count()

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
    
# ==========================================================
#                LISTING APPROVAL VIEWS
# ==========================================================

@login_required
def listing_approval_requests(request):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    listings = Listing.objects.filter(
        is_approved=False
    )

    return render(
        request,
        'properties/listing_approval_requests.html',
        {
            'listings': listings
        }
    )
    

@login_required
def approve_listing(request, listing_id):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    listing.is_approved = True
    listing.save()

    messages.success(
        request,
        'Listing approved successfully.'
    )

    return redirect(
        'listing_approval_requests'
    )
    
    
@login_required
def reject_listing(request, listing_id):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    listing.delete()

    messages.warning(
        request,
        'Listing rejected and deleted.'
    )

    return redirect(
        'listing_approval_requests'
    ) 
    
# ==========================================================
#                        API VIEWS
# ==========================================================


# ==========================================================
#                    PUBLIC APIs
# ==========================================================

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

    query = request.GET.get('q')

    category = request.GET.get('category')

    location = request.GET.get('location')

    min_price = request.GET.get('min_price')

    max_price = request.GET.get('max_price')

    ordering = request.GET.get(
        'ordering',
        '-created_at'
    )

    if query:

        listings = listings.filter(

            Q(title__icontains=query) |

            Q(description__icontains=query)

        )

    if category:

        listings = listings.filter(
            category_id=category
        )

    if location:

        listings = listings.filter(
            location__icontains=location
        )

    if min_price:

        listings = listings.filter(
            price__gte=min_price
        )

    if max_price:

        listings = listings.filter(
            price__lte=max_price
        )

    listings = listings.order_by(
        ordering
    )

    pagination = ListingPagination()

    result = pagination.paginate_queryset(
        listings,
        request
    )

    serializer = ListingSerializer(
        result,
        many=True,
        context={
            'request': request,
        }
    )

    return pagination.get_paginated_response(
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
        listing,
        context={
            'request': request,
        }
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
        many=True,
        context={
            'request': request,
        }
    )

    return Response(
        serializer.data
    )


@api_view(['GET'])
def api_recent_listings(request):

    listings = Listing.objects.filter(
        is_active=True,
        is_approved=True
    ).order_by(
        '-created_at'
    )[:10]

    serializer = ListingSerializer(
        listings,
        many=True,
        context={
            'request': request,
        }
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
        many=True,
        context={
            'request': request,
        }
    )

    return Response(
        serializer.data
    )
    
@api_view(['GET'])
def api_home(request):

    featured = Listing.objects.filter(
        is_active=True,
        is_approved=True,
        is_featured=True
    )[:6]

    recent = Listing.objects.filter(
        is_active=True,
        is_approved=True
    ).order_by(
        '-created_at'
    )[:6]

    categories = Category.objects.all()

    return Response(
        {
            'featured_listings': ListingSerializer(
                featured,
                many=True,
                context={
                    'request': request,
                }
            ).data,

            'recent_listings': ListingSerializer(
                recent,
                many=True,
                context={
                    'request': request,
                }
            ).data,

            'categories': CategorySerializer(
                categories,
                many=True
            ).data,
        }
    )


# ==========================================================
#                AUTHENTICATION APIs
# ==========================================================

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


# ==========================================================
#                 PROTECTED USER APIs
# ==========================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_listing(request):

    serializer = ListingCreateSerializer(
        data=request.data
    )

    if serializer.is_valid():

        listing = serializer.save(
            owner=request.user
        )

        return Response(
            ListingSerializer(listing).data,
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
        many=True,
        context={
            'request': request,
        }
    )

    return Response(
        serializer.data
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_favorites(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related(
        'listing'
    )

    listings = [
        favorite.listing
        for favorite in favorites
    ]

    serializer = ListingSerializer(
        listings,
        many=True,
        context={
            'request': request,
        }
    )

    return Response(
        serializer.data
    )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_toggle_favorite(
    request,
    listing_id
):

    listing = get_object_or_404(
        Listing,
        id=listing_id,
        is_active=True,
        is_approved=True
    )

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        listing=listing
    )

    if not created:

        favorite.delete()

        return Response(
            {
                'favorite': False,
                'message': 'Listing removed from favorites.'
            }
        )

    return Response(
        {
            'favorite': True,
            'message': 'Listing added to favorites.'
        }
    )
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_listing(
    request,
    listing_id
):

    listing = get_object_or_404(
        Listing,
        id=listing_id,
        owner=request.user
    )

    serializer = ListingCreateSerializer(
        listing,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=400
    )
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_listing(
    request,
    listing_id
):

    listing = get_object_or_404(
        Listing,
        id=listing_id,
        owner=request.user
    )

    listing.delete()

    return Response(
        {
            'message': 'Listing deleted successfully.'
        },
        status=200
    )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_upload_listing_image(
    request,
    listing_id
):

    listing = get_object_or_404(
        Listing,
        id=listing_id,
        owner=request.user
    )

    serializer = ListingImageCreateSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(
            listing=listing
        )

        return Response(
            serializer.data,
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_request_verification(request):

    existing_request = VerificationRequest.objects.filter(
        user=request.user,
        status='pending'
    ).exists()

    if existing_request:

        return Response(
            {
                'message': 'You already have a pending verification request.'
            },
            status=400
        )

    VerificationRequest.objects.create(
        user=request.user
    )

    return Response(
        {
            'message': 'Verification request submitted successfully.'
        },
        status=201
    )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_verification_status(request):

    verification_request = VerificationRequest.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    ).first()

    status = None

    if verification_request:

        status = verification_request.status

    return Response(
        {
            'is_verified': request.user.is_verified,
            'verification_status': status
        }
    )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):

    request.user.auth_token.delete()

    return Response(
        {
            'message': 'Logged out successfully.'
        }
    )
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_profile(request):

    serializer = UserUpdateSerializer(
        request.user,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data
        )

    return Response(
        serializer.errors,
        status=400
    )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_change_password(request):

    old_password = request.data.get(
        'old_password'
    )

    new_password = request.data.get(
        'new_password'
    )

    if not request.user.check_password(
        old_password
    ):

        return Response(
            {
                'error': 'Old password is incorrect.'
            },
            status=400
        )

    request.user.set_password(
        new_password
    )

    request.user.save()

    return Response(
        {
            'message': 'Password changed successfully.'
        }
    )
    
@api_view(['GET'])
def api_owner_profile(
    request,
    owner_id
):

    owner = get_object_or_404(
        User,
        id=owner_id
    )

    listings = Listing.objects.filter(
        owner=owner,
        is_active=True,
        is_approved=True
    )

    owner_data = UserSerializer(
        owner
    ).data

    listings_data = ListingSerializer(
        listings,
        many=True,
        context={
            'request': request,
        }
    ).data

    return Response(
        {
            'owner': owner_data,
            'listings': listings_data,
        }
    )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_dashboard(request):

    listings = Listing.objects.filter(
        owner=request.user
    )

    return Response(
        {
            'total_listings': listings.count(),
            'approved_listings': listings.filter(
                is_approved=True
            ).count(),
            'pending_listings': listings.filter(
                is_approved=False
            ).count(),
            'total_favorites': Favorite.objects.filter(
                user=request.user
            ).count(),
            'is_verified': request.user.is_verified,
        }
    )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_verification_requests(request):

    requests = VerificationRequest.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )

    serializer = VerificationRequestSerializer(
        requests,
        many=True
    )

    return Response(
        serializer.data
    )
    
# ==========================================================
#                    ADMIN APIs
# ==========================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_admin_statistics(request):

    if not request.user.is_superuser:

        return Response(
            {
                'error': 'Permission denied.'
            },
            status=403
        )

    return Response(
        {
            'total_users': User.objects.count(),

            'verified_users': User.objects.filter(
                is_verified=True
            ).count(),

            'total_categories': Category.objects.count(),

            'total_listings': Listing.objects.count(),

            'approved_listings': Listing.objects.filter(
                is_approved=True
            ).count(),

            'pending_listings': Listing.objects.filter(
                is_approved=False
            ).count(),

            'featured_listings': Listing.objects.filter(
                is_featured=True
            ).count(),
        }
    )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_listing_status(request):

    listings = Listing.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    data = []

    for listing in listings:

        data.append({

            'id': listing.id,

            'title': listing.title,

            'approved': listing.is_approved,

            'active': listing.is_active,

            'created_at': listing.created_at,

        })

    return Response(data)