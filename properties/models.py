from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

#==============================
# Name model representing a category of property listings
#==============================
class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):

        return self.name
    
    


class Region(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:

        ordering = (
            'name',
        )

    def __str__(self):

        return self.name


class District(models.Model):

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='districts'
    )

    name = models.CharField(
        max_length=100
    )

    class Meta:

        ordering = (
            'name',
        )

        unique_together = (
            'region',
            'name'
        )

    def __str__(self):

        return f"{self.name}, {self.region.name}"


class Ward(models.Model):

    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='wards'
    )

    name = models.CharField(
        max_length=100
    )

    class Meta:

        ordering = (
            'name',
        )

        unique_together = (
            'district',
            'name'
        )

    def __str__(self):

        return f"{self.name}, {self.district.name}"


class StreetArea(models.Model):

    ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        related_name='streets'
    )

    name = models.CharField(
        max_length=100
    )

    class Meta:

        ordering = (
            'name',
        )

        unique_together = (
            'ward',
            'name'
        )

    def __str__(self):

        return f"{self.name}, {self.ward.name}"


#==============================
# Listing model representing a property listing
#==============================
class Listing(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('pending', 'Pending Confirmation'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('airtel_money', 'Airtel Money'),
        ('halopesa', 'HaloPesa'),
        ('yas', 'Yas'),
        ('credit_card', 'Credit Card'),
    ]

    AVAILABILITY_STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('sold', 'Sold'),
        ('hired', 'Hired'),
        ('unavailable', 'Unavailable'),
    ]

    FEATURED_PACKAGE_CHOICES = [
        ('featured_7', 'Featured - 7 days'),
        ('premium_30', 'Premium - 30 days'),
        ('spotlight_30', 'Homepage Spotlight - 30 days'),
    ]

    FEATURED_PACKAGES = {
        'featured_7': {
            'name': 'Featured',
            'duration_days': 7,
            'price': Decimal('5000'),
        },
        'premium_30': {
            'name': 'Premium',
            'duration_days': 30,
            'price': Decimal('15000'),
        },
        'spotlight_30': {
            'name': 'Homepage Spotlight',
            'duration_days': 30,
            'price': Decimal('25000'),
        },
    }

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    location = models.CharField(
        max_length=200
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    ward = models.ForeignKey(
        Ward,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    street_area = models.ForeignKey(
        StreetArea,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    location_description = models.CharField(
        max_length=200,
        blank=True
    )
    
    latitude = models.DecimalField(
        max_digits=12,
        decimal_places=8,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=12,
        decimal_places=8,
        null=True,
        blank=True
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    is_approved = models.BooleanField(
        default=False
    )
    
    is_featured = models.BooleanField(
        default=False
    )
    
    is_active = models.BooleanField(
        default=True
    )

    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_STATUS_CHOICES,
        default='available'
    )

    publishing_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid'
    )

    payment_reference = models.CharField(
        max_length=100,
        blank=True
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True
    )

    payment_note = models.TextField(
        blank=True
    )

    featured_package = models.CharField(
        max_length=30,
        choices=FEATURED_PACKAGE_CHOICES,
        blank=True
    )

    payment_rejection_reason = models.TextField(
        blank=True
    )

    listing_rejection_reason = models.TextField(
        blank=True
    )

    owner_id_document = models.ImageField(
        upload_to='listing_owner_ids/',
        blank=True,
        null=True
    )

    payment_submitted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    featured_until = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        full_location = self.get_full_location()

        if full_location:

            self.location = full_location

        super().save(*args, **kwargs)

    def get_full_location(self):

        if (
            self.street_area
            and self.ward
            and self.district
            and self.region
        ):

            return (
                f'{self.street_area.name}, {self.ward.name}, '
                f'{self.district.name}, {self.region.name}'
            )

        return self.location

    def set_featured_package_price(self):

        if self.featured_package in self.FEATURED_PACKAGES:

            self.publishing_fee = self.FEATURED_PACKAGES[
                self.featured_package
            ]['price']

    @property
    def is_featured_active(self):

        if not self.is_featured:

            return False

        if self.featured_until is None:

            return True

        return self.featured_until >= timezone.now()

    def __str__(self):

        return self.title


class PublishingPaymentMethod(models.Model):

    code = models.CharField(
        max_length=30,
        choices=Listing.PAYMENT_METHOD_CHOICES,
        unique=True
    )

    name = models.CharField(
        max_length=80
    )

    lipa_number = models.CharField(
        max_length=100,
        blank=True
    )

    instructions = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    sort_order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = (
            'sort_order',
            'name'
        )

    def __str__(self):

        return self.name
    
#==============================
# ListingImage model representing an image of a property listing
#==============================
class ListingImage(models.Model):

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='listing_images/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Image for {self.listing.title}"  
    
class Favorite(models.Model):

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'user',
            'listing'
        )

    def __str__(self):

        return f"{self.user.username} - {self.listing.title}"


class ContactUnlock(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('pending', 'Pending Confirmation'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='contact_unlocks'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=500
    )

    is_paid = models.BooleanField(
        default=False
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid'
    )

    payment_method = models.CharField(
        max_length=30,
        choices=Listing.PAYMENT_METHOD_CHOICES,
        blank=True
    )

    payment_reference = models.CharField(
        max_length=100,
        blank=True
    )

    payment_note = models.TextField(
        blank=True
    )

    payment_rejection_reason = models.TextField(
        blank=True
    )

    payment_submitted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    unlocked_at = models.DateTimeField(
        blank=True,
        null=True
    )

    expires_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        unique_together = (
            'user',
            'listing'
        )

    @property
    def is_active_unlock(self):

        if not self.is_paid:

            return False

        if not self.expires_at:

            return False

        return self.expires_at > timezone.now()

    def __str__(self):

        return f"{self.user} unlocked {self.listing}"


class VerificationRequest(models.Model):

    STATUS_CHOICES = [

        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),

    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    id_document = models.ImageField(
        upload_to='verification_ids/',
        blank=True,
        null=True
    )

    rejection_reason = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.status}"  
