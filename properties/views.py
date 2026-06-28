from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .forms import (
    ContactUnlockPaymentForm,
    ListingForm,
    ListingImageForm,
    ListingPaymentForm,
    ManualFeaturedListingForm,
    RejectionReasonForm,
)
from accounts.forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Case, IntegerField, Q, Value, When
from django.core.paginator import Paginator
from accounts.models import User
from dalalimtandaoni.cloudinary_uploads import upload_image_to_cloudinary
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from .models import Favorite
from django.http import HttpResponseForbidden
from django.http import JsonResponse
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
    parser_classes,
    permission_classes
)
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from .serializers import (
    CategorySerializer,
    ListingSerializer,
    UserRegisterSerializer,
    ListingCreateSerializer,
    ListingPaymentSerializer,
    PublishingPaymentMethodSerializer,
    RegionSerializer,
    DistrictSerializer,
    WardSerializer,
    StreetAreaSerializer,
    UserSerializer,
    UserUpdateSerializer,
    ListingImageCreateSerializer,
)

from .models import (
    Listing,
    Category,
    ContactUnlock,
    District,
    Favorite,
    PublishingPaymentMethod,
    Region,
    StreetArea,
    Ward,

)
from .validators import validate_image_upload
from .rate_limits import rate_limit

# ==========================================================
#                     HELPER FUNCTIONS
# ==========================================================
def active_featured_q():

    return Q(is_featured=True) & (
        Q(featured_until__isnull=True) |
        Q(featured_until__gte=timezone.now())
    )


def order_featured_first(queryset, *order_fields):

    return queryset.annotate(
        featured_priority=Case(
            When(
                active_featured_q(),
                then=Value(1)
            ),
            default=Value(0),
            output_field=IntegerField()
        )
    ).order_by(
        '-featured_priority',
        *order_fields
    )


def apply_featured_package(
    listing,
    package_key=None,
    featured_until=None
):

    if package_key in Listing.FEATURED_PACKAGES:

        listing.featured_package = package_key

    elif not listing.featured_package:

        listing.featured_package = 'featured_7'

    package = Listing.FEATURED_PACKAGES.get(
        listing.featured_package,
        Listing.FEATURED_PACKAGES['featured_7']
    )

    listing.is_featured = True

    if featured_until:

        listing.featured_until = featured_until

    else:

        listing.featured_until = timezone.now() + timedelta(
            days=package['duration_days']
        )

    listing.set_featured_package_price()


def parse_admin_featured_until(value):

    if not value:

        return None

    featured_until = parse_datetime(
        str(value)
    )

    if featured_until and timezone.is_naive(featured_until):

        featured_until = timezone.make_aware(
            featured_until,
            timezone.get_current_timezone()
        )

    return featured_until


def format_whatsapp_number(phone):

    if phone.startswith('0'):
        return '255' + phone[1:]

    return phone


def _location_option_data(queryset):

    return [
        {
            'id': item.id,
            'name': item.name,
        }
        for item in queryset
    ]

# ==========================================================
#                     PUBLIC VIEWS
# ==========================================================
def location_districts(request):

    region_id = request.GET.get(
        'region'
    )

    districts = District.objects.none()

    if region_id:

        districts = District.objects.filter(
            region_id=region_id
        )

    return JsonResponse(
        {
            'results': _location_option_data(
                districts
            )
        }
    )


def location_wards(request):

    district_id = request.GET.get(
        'district'
    )

    wards = Ward.objects.none()

    if district_id:

        wards = Ward.objects.filter(
            district_id=district_id
        )

    return JsonResponse(
        {
            'results': _location_option_data(
                wards
            )
        }
    )


def location_streets(request):

    ward_id = request.GET.get(
        'ward'
    )

    streets = StreetArea.objects.none()

    if ward_id:

        streets = StreetArea.objects.filter(
            ward_id=ward_id
        )

    return JsonResponse(
        {
            'results': _location_option_data(
                streets
            )
        }
    )


def home(request):

    featured_listings = Listing.objects.filter(
        is_active=True,
        is_approved=True,
        availability_status='available',
        is_featured=True
    ).filter(active_featured_q())[:6]

    total_listings = Listing.objects.filter(
        is_active=True,
        is_approved=True,
        availability_status='available'
    ).count()

    total_users = User.objects.count()

    total_categories = Category.objects.count()

    approved_listings = Listing.objects.filter(
        is_active=True,
        is_approved=True,
        availability_status='available'
    ).count()

    recent_listings = Listing.objects.filter(
        is_active=True,
        is_approved=True,
        availability_status='available'
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
            'approved_listings': approved_listings,
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


def terms(request):

    return render(
        request,
        'properties/terms.html'
    )


def privacy(request):

    return render(
        request,
        'properties/privacy.html'
    )


def listing_rules(request):

    return render(
        request,
        'properties/listing_rules.html'
    )


def custom_404(request, exception):

    return render(
        request,
        '404.html',
        status=404
    )


def custom_403(request, exception):

    return render(
        request,
        '403.html',
        status=403
    )


def custom_500(request):

    return render(
        request,
        '500.html',
        status=500
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

    region_id = request.GET.get(
        'region',
        ''
    )

    district_id = request.GET.get(
        'district',
        ''
    )

    ward_id = request.GET.get(
        'ward',
        ''
    )

    street_area_id = request.GET.get(
        'street_area',
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
        is_approved=True,

        availability_status='available'
    )

    if query:

        listings = listings.filter(

            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(location_description__icontains=query) |
            Q(region__name__icontains=query) |
            Q(district__name__icontains=query) |
            Q(ward__name__icontains=query) |
            Q(street_area__name__icontains=query)

        )

    if category_id:

        listings = listings.filter(
            category_id=category_id
        )

    if region_id:

        listings = listings.filter(
            region_id=region_id
        )

    if district_id:

        listings = listings.filter(
            district_id=district_id
        )

    if ward_id:

        listings = listings.filter(
            ward_id=ward_id
        )

    if street_area_id:

        listings = listings.filter(
            street_area_id=street_area_id
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

        listings = order_featured_first(
            listings,
            "price"
        )

    elif sort == "price_high":

        listings = order_featured_first(
            listings,
            "-price"
        )

    elif sort == "oldest":

        listings = order_featured_first(
            listings,
            "created_at"
        )

    else:

        listings = order_featured_first(
            listings,
            "-created_at"
        )

    categories = Category.objects.all()
    regions = Region.objects.all()
    districts = District.objects.filter(
        region_id=region_id
    ) if region_id else District.objects.none()
    wards = Ward.objects.filter(
        district_id=district_id
    ) if district_id else Ward.objects.none()
    streets = StreetArea.objects.filter(
        ward_id=ward_id
    ) if ward_id else StreetArea.objects.none()

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
            'regions': regions,
            'districts': districts,
            'wards': wards,
            'streets': streets,
            'query': query,
            'selected_category': category_id,
            'selected_region': region_id,
            'selected_district': district_id,
            'selected_ward': ward_id,
            'selected_street_area': street_area_id,
            'min_price': min_price,
            'max_price': max_price,
            'sort': sort,
        }
    )

def listing_detail(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk
    )

    if (
        not listing.is_active
        or listing.availability_status != 'available'
        or not listing.is_approved
    ) and (
        not request.user.is_authenticated
        or (
            request.user != listing.owner
            and not request.user.is_superuser
        )
    ):

        return HttpResponseForbidden()

    is_favorite = False

    if request.user.is_authenticated:

        is_favorite = Favorite.objects.filter(
            user=request.user,
            listing=listing
        ).exists()

    contact_unlock = None
    can_view_contact = False

    if request.user.is_authenticated:

        if request.user == listing.owner or request.user.is_superuser:

            can_view_contact = True

        else:

            contact_unlock = ContactUnlock.objects.filter(
                user=request.user,
                listing=listing
            ).first()

            if contact_unlock and contact_unlock.is_active_unlock:

                can_view_contact = True

    whatsapp_number = ''

    if can_view_contact:

        whatsapp_number = format_whatsapp_number(
            listing.owner.phone_number
        )

    related_listings = Listing.objects.filter(
        category=listing.category,
        is_active=True,
        is_approved=True,
        availability_status='available'
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
            'can_view_contact': can_view_contact,
            'contact_unlock': contact_unlock,
            'contact_unlock_fee': settings.CONTACT_UNLOCK_FEE,
            'contact_unlock_days': settings.CONTACT_UNLOCK_DAYS,
            'related_listings': related_listings,

        }
    )


@login_required
def unlock_contact(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk,
        is_active=True,
        is_approved=True,
        availability_status='available'
    )

    if request.user == listing.owner or request.user.is_superuser:

        return redirect(
            'listing_detail',
            pk=listing.pk
        )

    unlock, created = ContactUnlock.objects.get_or_create(
        user=request.user,
        listing=listing
    )

    if unlock.is_active_unlock:

        messages.info(
            request,
            'You have already unlocked this contact.'
        )

        return redirect(
            'listing_detail',
            pk=listing.pk
        )

    if request.method == 'POST':

        form = ContactUnlockPaymentForm(
            request.POST,
            instance=unlock
        )

        if form.is_valid():

            contact_unlock = form.save(
                commit=False
            )

            contact_unlock.amount = settings.CONTACT_UNLOCK_FEE
            contact_unlock.is_paid = False
            contact_unlock.payment_status = 'pending'
            contact_unlock.payment_submitted_at = timezone.now()
            contact_unlock.payment_rejection_reason = ''
            contact_unlock.unlocked_at = None
            contact_unlock.expires_at = None
            contact_unlock.save()

            messages.success(
                request,
                (
                    'Contact unlock payment submitted. Admin will confirm '
                    'it before the phone number is unlocked.'
                )
            )

            return redirect(
                'listing_detail',
                pk=listing.pk
            )

    else:

        form = ContactUnlockPaymentForm(
            instance=unlock
        )

    payment_methods = PublishingPaymentMethod.objects.filter(
        is_active=True
    ).order_by(
        'sort_order',
        'name'
    )

    payment_methods_json = [
        {
            'code': method.code,
            'name': method.name,
            'lipa_number': method.lipa_number,
            'instructions': method.instructions,
        }
        for method in payment_methods
    ]

    return render(
        request,
        'properties/unlock_contact.html',
        {
            'form': form,
            'listing': listing,
            'unlock': unlock,
            'contact_unlock_fee': settings.CONTACT_UNLOCK_FEE,
            'contact_unlock_days': settings.CONTACT_UNLOCK_DAYS,
            'payment_methods_json': payment_methods_json,
        }
    )

@login_required
def create_listing(request):

    if request.method == 'POST':

        form = ListingForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            listing = form.save(
                commit=False
            )

            listing.owner = request.user

            listing.save()

            messages.success(
                request,
                'Listing submitted successfully. Admin will review it before publishing.'
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

            image.image_url = upload_image_to_cloudinary(
                form.cleaned_data.get('image'),
                'listing_images'
            )

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
def submit_listing_payment(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk,
        owner=request.user
    )

    if listing.payment_status == 'paid' and listing.is_featured_active:

        messages.info(
            request,
            'This listing is already featured.'
        )

        return redirect(
            'my_listings'
        )

    if request.method == 'POST':

        form = ListingPaymentForm(
            request.POST,
            instance=listing
        )

        if form.is_valid():

            payment = form.save(
                commit=False
            )

            payment.set_featured_package_price()
            payment.payment_status = 'pending'
            payment.payment_submitted_at = timezone.now()
            payment.payment_rejection_reason = ''
            payment.save()

            messages.success(
                request,
                'Featured listing payment submitted. Admin will confirm it before promotion starts.'
            )

            return redirect(
                'my_listings'
            )

    else:

        form = ListingPaymentForm(
            instance=listing
        )

    payment_methods = PublishingPaymentMethod.objects.filter(
        is_active=True
    ).order_by(
        'sort_order',
        'name'
    )

    payment_methods_json = [
        {
            'code': method.code,
            'name': method.name,
            'lipa_number': method.lipa_number,
            'instructions': method.instructions,
        }
        for method in payment_methods
    ]

    return render(
        request,
        'properties/submit_listing_payment.html',
        {
            'form': form,
            'listing': listing,
            'payment_methods_json': payment_methods_json,
        }
    )

@login_required
def my_listings(request):

    listings = Listing.objects.filter(
        owner=request.user
    ).order_by(
        '-created_at'
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
            request.FILES,
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

        listing.is_active = False
        listing.availability_status = 'unavailable'
        listing.save()

        messages.success(
            request,
            'Listing removed from public view.'
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
def update_listing_availability(request, pk, status):

    valid_statuses = {
        choice[0]
        for choice in Listing.AVAILABILITY_STATUS_CHOICES
    }

    if status not in valid_statuses:

        return HttpResponseForbidden()

    listing = get_object_or_404(
        Listing,
        pk=pk,
        owner=request.user
    )

    if request.method != 'POST':

        return redirect(
            'my_listings'
        )

    listing.availability_status = status

    if status == 'available':

        listing.is_active = True

    listing.save()

    messages.success(
        request,
        f'Listing marked as {listing.get_availability_status_display()}.'
    )

    return redirect(
        'my_listings'
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

    pending_payment_listings = listings.filter(
        payment_status='pending'
    ).count()

    total_favorites = Favorite.objects.filter(
        user=request.user
    ).count()

    contact_unlock_count = ContactUnlock.objects.filter(
        listing__owner=request.user,
        is_paid=True
    ).count()

    return render(
        request,
        'properties/dashboard.html',
        {
            'total_listings': total_listings,
            'approved_listings': approved_listings,
            'pending_listings': pending_listings,
            'pending_payment_listings': pending_payment_listings,
            'total_favorites': total_favorites,
            'contact_unlock_count': contact_unlock_count,
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
        is_approved=True,

        availability_status='available'
    )

    can_view_owner_contact = (
        request.user.is_authenticated
        and (
            request.user == owner
            or request.user.is_superuser
        )
    )

    whatsapp_number = ''

    if can_view_owner_contact:

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
            'can_view_owner_contact': can_view_owner_contact,
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


@login_required
def my_profile(request):

    if request.method == 'POST':

        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            user = request.user

            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.phone_number = form.cleaned_data.get('phone_number')

            profile_picture = request.FILES.get('profile_picture')

            if profile_picture:

                cloudinary_url = upload_image_to_cloudinary(
                    profile_picture,
                    'profile_pictures'
                )

                if cloudinary_url:
                    user.profile_picture_url = cloudinary_url

            user.save()

            messages.success(
                request,
                'Profile updated successfully.'
            )

            return redirect('my_profile')

        messages.error(
            request,
            'Please correct the highlighted profile details.'
        )

    else:

        form = UserProfileForm(
            instance=request.user
        )

    listings = Listing.objects.filter(
        owner=request.user,
        is_active=True,
        is_approved=True,
        availability_status='available'
    )

    whatsapp_number = format_whatsapp_number(
        request.user.phone_number
    )

    return render(
        request,
        'properties/owner_profile.html',
        {
            'owner': request.user,
            'listings': listings,
            'listing_count': listings.count(),
            'whatsapp_number': whatsapp_number,
            'form': form,
            'is_my_profile': True,
            'can_view_owner_contact': True,
        }
    )



# ==========================================================
#                LISTING APPROVAL VIEWS
# ==========================================================

@login_required
def listing_approval_requests(request):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    listings = Listing.objects.filter(
        is_approved=False,
        availability_status='available'
    )

    return render(
        request,
        'properties/listing_approval_requests.html',
        {
            'listings': listings,
            'featured_package_choices': Listing.FEATURED_PACKAGE_CHOICES,
        }
    )


@login_required
def featured_listing_management(request):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    listings = Listing.objects.filter(
        is_approved=True
    ).select_related(
        'owner',
        'category'
    ).order_by(
        '-is_featured',
        '-created_at'
    )

    return render(
        request,
        'properties/featured_listing_management.html',
        {
            'listings': listings,
            'featured_package_choices': Listing.FEATURED_PACKAGE_CHOICES,
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
def toggle_featured_listing(request, listing_id):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    if request.method != 'POST':

        messages.warning(
            request,
            'Choose a featured package and time limit before marking a listing as featured.'
        )

        return redirect(
            request.META.get(
                'HTTP_REFERER',
                'featured_listing_management'
            )
        )

    action = request.POST.get(
        'action',
        'mark'
    )

    if action == 'remove':

        listing.is_featured = False
        listing.featured_until = None
        listing.save()

        messages.info(
            request,
            'Listing removed from featured listings.'
        )

    else:

        form = ManualFeaturedListingForm(
            request.POST
        )

        if not form.is_valid():

            for errors in form.errors.values():

                for error in errors:

                    messages.error(
                        request,
                        error
                    )

        else:

            apply_featured_package(
                listing,
                form.cleaned_data['featured_package'],
                form.cleaned_data.get(
                    'featured_until'
                )
            )
            listing.save()

            messages.success(
                request,
                'Listing marked as featured with a time limit.'
            )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'featured_listing_management'
        )
    )


@login_required
def payment_confirmation_requests(request):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    listings = Listing.objects.filter(
        payment_status='pending'
    ).order_by(
        '-payment_submitted_at'
    )

    return render(
        request,
        'properties/payment_confirmation_requests.html',
        {
            'listings': listings
        }
    )


@login_required
def approve_listing_payment(request, listing_id):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    listing.payment_status = 'paid'
    listing.paid_at = timezone.now()
    listing.payment_rejection_reason = ''

    apply_featured_package(
        listing,
        listing.featured_package
    )

    listing.save()

    messages.success(
        request,
        'Featured listing payment confirmed. Listing is now promoted.'
    )

    return redirect(
        'payment_confirmation_requests'
    )


@login_required
def reject_listing_payment(request, listing_id):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    if request.method == 'POST':

        form = RejectionReasonForm(
            request.POST
        )

        if form.is_valid():

            listing.payment_status = 'rejected'
            listing.payment_rejection_reason = form.cleaned_data['reason']
            listing.paid_at = None
            listing.save()

            messages.warning(
                request,
                'Featured listing payment rejected. Owner can submit a corrected reference.'
            )

            return redirect(
                'payment_confirmation_requests'
            )

    else:

        form = RejectionReasonForm()

    return render(
        request,
        'properties/reject_listing_payment.html',
        {
            'form': form,
            'listing': listing,
        }
    )


@login_required
def contact_unlock_payment_requests(request):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    unlocks = ContactUnlock.objects.filter(
        payment_status='pending'
    ).select_related(
        'user',
        'listing',
        'listing__owner'
    ).order_by(
        '-payment_submitted_at'
    )

    return render(
        request,
        'properties/contact_unlock_payment_requests.html',
        {
            'unlocks': unlocks
        }
    )


@login_required
def approve_contact_unlock_payment(request, unlock_id):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    unlock = get_object_or_404(
        ContactUnlock,
        id=unlock_id
    )

    unlock.amount = settings.CONTACT_UNLOCK_FEE
    unlock.is_paid = True
    unlock.payment_status = 'paid'
    unlock.payment_rejection_reason = ''
    unlock.unlocked_at = timezone.now()
    unlock.expires_at = timezone.now() + timedelta(
        days=settings.CONTACT_UNLOCK_DAYS
    )
    unlock.save()

    # TODO: Notify owner when a user unlocks their contact.

    messages.success(
        request,
        'Contact unlock payment confirmed. Contact is now unlocked.'
    )

    return redirect(
        'contact_unlock_payment_requests'
    )


@login_required
def reject_contact_unlock_payment(request, unlock_id):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    unlock = get_object_or_404(
        ContactUnlock,
        id=unlock_id
    )

    if request.method == 'POST':

        form = RejectionReasonForm(
            request.POST
        )

        if form.is_valid():

            unlock.payment_status = 'rejected'
            unlock.is_paid = False
            unlock.unlocked_at = None
            unlock.expires_at = None
            unlock.payment_rejection_reason = form.cleaned_data['reason']
            unlock.save()

            messages.warning(
                request,
                'Contact unlock payment rejected. User can submit a corrected reference.'
            )

            return redirect(
                'contact_unlock_payment_requests'
            )

    else:

        form = RejectionReasonForm()

    return render(
        request,
        'properties/reject_contact_unlock_payment.html',
        {
            'form': form,
            'unlock': unlock,
        }
    )


@login_required
def reject_listing(request, listing_id):

    if not request.user.is_superuser:

        return HttpResponseForbidden()

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    if request.method == 'POST':

        form = RejectionReasonForm(
            request.POST
        )

        if form.is_valid():

            listing.is_approved = False
            listing.is_active = False
            listing.listing_rejection_reason = form.cleaned_data['reason']
            listing.save()

            messages.warning(
                request,
                'Listing rejected.'
            )

            return redirect(
                'listing_approval_requests'
            )

    else:

        form = RejectionReasonForm()

    return render(
        request,
        'properties/reject_listing.html',
        {
            'form': form,
            'listing': listing,
        }
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
def api_regions(request):

    serializer = RegionSerializer(
        Region.objects.all(),
        many=True
    )

    return Response(
        serializer.data
    )


@api_view(['GET'])
def api_districts(request):

    region_id = request.GET.get(
        'region'
    )

    districts = District.objects.none()

    if region_id:

        districts = District.objects.filter(
            region_id=region_id
        )

    serializer = DistrictSerializer(
        districts,
        many=True
    )

    return Response(
        serializer.data
    )


@api_view(['GET'])
def api_wards(request):

    district_id = request.GET.get(
        'district'
    )

    wards = Ward.objects.none()

    if district_id:

        wards = Ward.objects.filter(
            district_id=district_id
        )

    serializer = WardSerializer(
        wards,
        many=True
    )

    return Response(
        serializer.data
    )


@api_view(['GET'])
def api_streets(request):

    ward_id = request.GET.get(
        'ward'
    )

    streets = StreetArea.objects.none()

    if ward_id:

        streets = StreetArea.objects.filter(
            ward_id=ward_id
        )

    serializer = StreetAreaSerializer(
        streets,
        many=True
    )

    return Response(
        serializer.data
    )


@api_view(['GET'])
def api_listings(request):

    listings = Listing.objects.filter(
        is_active=True,
        is_approved=True,

        availability_status='available'
    )

    query = request.GET.get('q')

    category = request.GET.get('category')

    location = request.GET.get('location')
    region = request.GET.get('region')
    district = request.GET.get('district')
    ward = request.GET.get('ward')
    street_area = request.GET.get('street_area')

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
            Q(location__icontains=location) |
            Q(location_description__icontains=location)
        )

    if region:

        listings = listings.filter(
            region_id=region
        )

    if district:

        listings = listings.filter(
            district_id=district
        )

    if ward:

        listings = listings.filter(
            ward_id=ward
        )

    if street_area:

        listings = listings.filter(
            street_area_id=street_area
        )

    if min_price:

        listings = listings.filter(
            price__gte=min_price
        )

    if max_price:

        listings = listings.filter(
            price__lte=max_price
        )

    listings = order_featured_first(
        listings,
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
        is_approved=True,

        availability_status='available'
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_unlock_contact(request, listing_id):

    listing = get_object_or_404(
        Listing,
        id=listing_id,
        is_active=True,
        is_approved=True,
        availability_status='available'
    )

    if request.user == listing.owner or request.user.is_superuser:

        serializer = ListingSerializer(
            listing,
            context={
                'request': request,
            }
        )

        return Response(
            {
                'message': 'You can already view this contact.',
                'listing': serializer.data,
            }
        )

    unlock, created = ContactUnlock.objects.get_or_create(
        user=request.user,
        listing=listing
    )

    if unlock.is_active_unlock:

        serializer = ListingSerializer(
            listing,
            context={
                'request': request,
            }
        )

        return Response(
            {
                'message': 'You have already unlocked this contact.',
                'listing': serializer.data,
            }
        )

    payment_method = request.data.get(
        'payment_method',
        ''
    ).strip()

    payment_reference = request.data.get(
        'payment_reference',
        ''
    ).strip()

    payment_note = request.data.get(
        'payment_note',
        ''
    ).strip()

    if not payment_method:

        return Response(
            {
                'payment_method': 'Please choose the payment method used.'
            },
            status=400
        )

    if not PublishingPaymentMethod.objects.filter(
        code=payment_method,
        is_active=True
    ).exists():

        return Response(
            {
                'payment_method': 'Please choose an active payment method.'
            },
            status=400
        )

    if not payment_reference:

        return Response(
            {
                'payment_reference': 'Please enter the payment reference.'
            },
            status=400
        )

    unlock.amount = settings.CONTACT_UNLOCK_FEE
    unlock.is_paid = False
    unlock.payment_status = 'pending'
    unlock.payment_method = payment_method
    unlock.payment_reference = payment_reference
    unlock.payment_note = payment_note
    unlock.payment_rejection_reason = ''
    unlock.payment_submitted_at = timezone.now()
    unlock.unlocked_at = None
    unlock.expires_at = None
    unlock.save()

    serializer = ListingSerializer(
        listing,
        context={
            'request': request,
        }
    )

    return Response(
        {
            'message': (
                'Contact unlock payment submitted. Admin will confirm it '
                'before the phone number is unlocked.'
            ),
            'listing': serializer.data,
        }
    )


@api_view(['GET'])
def api_featured_listings(request):

    listings = Listing.objects.filter(
        is_active=True,
        is_approved=True,

        availability_status='available',
        is_featured=True
    ).filter(active_featured_q())

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
        is_approved=True,

        availability_status='available'
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
        is_approved=True,

        availability_status='available'
    )

    if query:

        listings = listings.filter(

            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(location_description__icontains=query) |
            Q(region__name__icontains=query) |
            Q(district__name__icontains=query) |
            Q(ward__name__icontains=query) |
            Q(street_area__name__icontains=query)

        )

    serializer = ListingSerializer(
        order_featured_first(
            listings,
            '-created_at'
        ),
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

        availability_status='available',
        is_featured=True
    ).filter(active_featured_q())[:6]

    recent = Listing.objects.filter(
        is_active=True,
        is_approved=True,

        availability_status='available'
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
@rate_limit('api-register', limit=5, window=600)
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
@rate_limit('api-login', limit=10, window=300)
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
@parser_classes([MultiPartParser, FormParser])
def api_create_listing(request):

    serializer = ListingCreateSerializer(
        data=request.data
    )

    if serializer.is_valid():

        listing = serializer.save(
            owner=request.user
        )

        return Response(
            ListingSerializer(
                listing,
                context={
                    'request': request,
                }
            ).data,
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
        request.user,
        context={
            'request': request,
        }
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_submit_listing_payment(
    request,
    listing_id
):

    listing = get_object_or_404(
        Listing,
        id=listing_id,
        owner=request.user
    )

    if listing.payment_status == 'paid' and listing.is_featured_active:

        return Response(
            {
                'message': 'This listing is already featured.'
            },
            status=400
        )

    serializer = ListingPaymentSerializer(
        listing,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():

        payment = serializer.save(
            payment_status='pending',
            payment_submitted_at=timezone.now(),
            payment_rejection_reason=''
        )

        payment.set_featured_package_price()
        payment.save()

        return Response(
            ListingSerializer(
                payment,
                context={
                    'request': request,
                }
            ).data
        )

    return Response(
        serializer.errors,
        status=400
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_payment_methods(request):

    payment_methods = PublishingPaymentMethod.objects.filter(
        is_active=True
    ).order_by(
        'sort_order',
        'name'
    )

    serializer = PublishingPaymentMethodSerializer(
        payment_methods,
        many=True
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
        is_approved=True,

        availability_status='available'
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
@parser_classes([JSONParser, MultiPartParser, FormParser])
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

    listing.is_active = False
    listing.availability_status = 'unavailable'
    listing.save()

    return Response(
        {
            'message': 'Listing removed from public view.'
        },
        status=200
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_update_listing_availability(
    request,
    listing_id
):

    listing = get_object_or_404(
        Listing,
        id=listing_id,
        owner=request.user
    )

    status = request.data.get(
        'availability_status'
    )

    valid_statuses = {
        choice[0]
        for choice in Listing.AVAILABILITY_STATUS_CHOICES
    }

    if status not in valid_statuses:

        return Response(
            {
                'availability_status': 'Choose a valid availability status.'
            },
            status=400
        )

    listing.availability_status = status

    if status == 'available':

        listing.is_active = True

    listing.save()

    return Response(
        ListingSerializer(
            listing,
            context={
                'request': request,
            }
        ).data
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
        data=request.data,
        context={
            'request': request,
        }
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
def api_logout(request):

    request.user.auth_token.delete()

    return Response(
        {
            'message': 'Logged out successfully.'
        }
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def api_update_profile(request):

    serializer = UserUpdateSerializer(
        request.user,
        data=request.data,
        context={
            'request': request,
        },
        partial=True
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
@rate_limit('api-change-password', limit=5, window=600)
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
        is_approved=True,

        availability_status='available'
    )

    owner_data = UserSerializer(
        owner,
        context={
            'request': request,
        }
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
            'pending_payment_listings': listings.filter(
                payment_status='pending'
            ).count(),
            'contact_unlock_count': ContactUnlock.objects.filter(
                listing__owner=request.user,
                is_paid=True
            ).count(),
            'total_favorites': Favorite.objects.filter(
                user=request.user
            ).count(),
        }
    )


# ==========================================================
#                    ADMIN APIs
# ==========================================================
def _require_admin_api(request):

    if request.user.is_superuser:

        return None

    return Response(
        {
            'error': 'Permission denied.'
        },
        status=403
    )


def _get_required_rejection_reason(request):

    reason = request.data.get(
        'reason',
        ''
    ).strip()

    if reason:

        return reason, None

    return None, Response(
        {
            'reason': 'Please provide a rejection reason.'
        },
        status=400
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_admin_statistics(request):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    return Response(
        {
            'total_users': User.objects.count(),

            'total_categories': Category.objects.count(),

            'total_listings': Listing.objects.count(),

            'approved_listings': Listing.objects.filter(
                is_approved=True
            ).count(),

            'pending_listings': Listing.objects.filter(
                is_approved=False
            ).count(),
            'pending_payment_listings': Listing.objects.filter(
                payment_status='pending'
            ).count(),

            'featured_listings': Listing.objects.filter(
                is_featured=True
            ).filter(active_featured_q()).count(),
        }
    )




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_admin_featured_listing_management(request):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    listings = Listing.objects.filter(
        is_approved=True
    ).select_related(
        'owner',
        'category'
    ).order_by(
        '-is_featured',
        '-created_at'
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_admin_approve_listing(
    request,
    listing_id
):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    listing.is_approved = True
    listing.save()

    serializer = ListingSerializer(
        listing,
        context={
            'request': request,
        }
    )

    return Response(
        {
            'message': 'Listing approved successfully.',
            'listing': serializer.data,
        }
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_admin_reject_listing(
    request,
    listing_id
):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    reason, error_response = _get_required_rejection_reason(
        request
    )

    if error_response is not None:

        return error_response

    listing.is_approved = False
    listing.is_active = False
    listing.listing_rejection_reason = reason
    listing.save()

    return Response(
        {
            'message': 'Listing rejected.'
        }
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_admin_toggle_featured_listing(
    request,
    listing_id
):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    is_featured = request.data.get(
        'is_featured'
    )

    if is_featured is None:

        listing.is_featured = not listing.is_featured

    else:

        listing.is_featured = str(
            is_featured
        ).lower() in (
            'true',
            '1',
            'yes'
        )

    if listing.is_featured:

        featured_until = parse_admin_featured_until(
            request.data.get(
                'featured_until'
            )
        )

        if request.data.get('featured_until') and featured_until is None:

            return Response(
                {
                    'error': 'Invalid featured_until datetime.'
                },
                status=400
            )

        if featured_until and featured_until <= timezone.now():

            return Response(
                {
                    'error': 'Featured expiry must be in the future.'
                },
                status=400
            )

        apply_featured_package(
            listing,
            request.data.get(
                'featured_package'
            ) or listing.featured_package or 'featured_7',
            featured_until
        )

    else:

        listing.featured_until = None

    listing.save()

    serializer = ListingSerializer(
        listing,
        context={
            'request': request,
        }
    )

    return Response(
        {
            'message': 'Featured status updated.',
            'listing': serializer.data,
        }
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_admin_payment_confirmation_requests(request):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    listings = Listing.objects.filter(
        payment_status='pending'
    ).select_related(
        'owner',
        'category'
    ).order_by(
        '-payment_submitted_at'
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
def api_admin_contact_unlock_payment_requests(request):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    unlocks = ContactUnlock.objects.filter(
        payment_status='pending'
    ).select_related(
        'user',
        'listing',
        'listing__owner'
    ).order_by(
        '-payment_submitted_at'
    )

    return Response(
        [
            {
                'id': unlock.id,
                'listing_id': unlock.listing.id,
                'listing_title': unlock.listing.title,
                'client': unlock.user.get_full_name() or unlock.user.username,
                'owner': unlock.listing.owner.get_full_name() or unlock.listing.owner.username,
                'amount': str(unlock.amount),
                'payment_method': unlock.payment_method,
                'payment_reference': unlock.payment_reference,
                'payment_note': unlock.payment_note,
                'payment_submitted_at': unlock.payment_submitted_at,
            }
            for unlock in unlocks
        ]
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_admin_approve_listing_payment(
    request,
    listing_id
):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    listing.payment_status = 'paid'
    listing.paid_at = timezone.now()
    listing.payment_rejection_reason = ''

    apply_featured_package(
        listing,
        listing.featured_package
    )

    listing.save()

    serializer = ListingSerializer(
        listing,
        context={
            'request': request,
        }
    )

    return Response(
        {
            'message': 'Featured listing payment confirmed. Listing is now promoted.',
            'listing': serializer.data,
        }
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_admin_reject_listing_payment(
    request,
    listing_id
):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    listing = get_object_or_404(
        Listing,
        id=listing_id
    )

    reason, error_response = _get_required_rejection_reason(
        request
    )

    if error_response is not None:

        return error_response

    listing.payment_status = 'rejected'
    listing.payment_rejection_reason = reason
    listing.paid_at = None
    listing.save()

    serializer = ListingSerializer(
        listing,
        context={
            'request': request,
        }
    )

    return Response(
        {
            'message': 'Featured listing payment rejected. Owner can submit a corrected reference.',
            'listing': serializer.data,
        }
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_admin_approve_contact_unlock_payment(
    request,
    unlock_id
):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    unlock = get_object_or_404(
        ContactUnlock,
        id=unlock_id
    )

    unlock.amount = settings.CONTACT_UNLOCK_FEE
    unlock.is_paid = True
    unlock.payment_status = 'paid'
    unlock.payment_rejection_reason = ''
    unlock.unlocked_at = timezone.now()
    unlock.expires_at = timezone.now() + timedelta(
        days=settings.CONTACT_UNLOCK_DAYS
    )
    unlock.save()

    return Response(
        {
            'message': 'Contact unlock payment confirmed. Contact is now unlocked.'
        }
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_admin_reject_contact_unlock_payment(
    request,
    unlock_id
):

    permission_error = _require_admin_api(
        request
    )

    if permission_error is not None:

        return permission_error

    unlock = get_object_or_404(
        ContactUnlock,
        id=unlock_id
    )

    reason = request.data.get(
        'reason',
        ''
    ).strip()

    unlock.payment_status = 'rejected'
    unlock.is_paid = False
    unlock.unlocked_at = None
    unlock.expires_at = None
    unlock.payment_rejection_reason = reason
    unlock.save()

    return Response(
        {
            'message': 'Contact unlock payment rejected. User can submit a corrected reference.'
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

            'availability_status': listing.availability_status,

            'payment_status': listing.payment_status,

            'payment_reference': listing.payment_reference,

            'payment_rejection_reason': listing.payment_rejection_reason,

            'listing_rejection_reason': listing.listing_rejection_reason,

            'created_at': listing.created_at,

        })

    return Response(data)