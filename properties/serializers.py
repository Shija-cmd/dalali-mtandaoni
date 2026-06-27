from rest_framework import serializers
from django.conf import settings
from django.utils import timezone

from .models import (
    Category,
    ContactUnlock,
    District,
    Listing,
    ListingImage,
    PublishingPaymentMethod,
    Region,
    StreetArea,
    VerificationRequest,
    Ward,
)

from accounts.models import User
from .validators import validate_image_upload


# ==========================================================
#                 CATEGORY SERIALIZER
# ==========================================================

class CategorySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Category

        fields = '__all__'


class PublishingPaymentMethodSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = PublishingPaymentMethod

        fields = [
            'code',
            'name',
            'lipa_number',
            'instructions',
        ]


class RegionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Region
        fields = [
            'id',
            'name',
        ]


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:

        model = District
        fields = [
            'id',
            'name',
            'region',
        ]


class WardSerializer(serializers.ModelSerializer):

    class Meta:

        model = Ward
        fields = [
            'id',
            'name',
            'district',
        ]


class StreetAreaSerializer(serializers.ModelSerializer):

    class Meta:

        model = StreetArea
        fields = [
            'id',
            'name',
            'ward',
        ]


# ==========================================================
#              LISTING IMAGE SERIALIZER
# ==========================================================

class ListingImageSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ListingImage

        fields = [
            'id',
            'image',
        ]


# ==========================================================
#                 LISTING SERIALIZER
# ==========================================================

class ListingSerializer(
    serializers.ModelSerializer
):

    category = serializers.StringRelatedField()
    
    category_id = serializers.IntegerField(
        source='category.id',
        read_only=True,
    )

    owner = serializers.StringRelatedField()

    owner_full_name = serializers.SerializerMethodField()

    owner_first_name = serializers.CharField(
        source='owner.first_name',
        read_only=True
    )

    owner_last_name = serializers.CharField(
        source='owner.last_name',
        read_only=True
    )

    owner_phone_number = serializers.CharField(
        source='owner.phone_number',
        read_only=True
    )

    can_view_contact = serializers.SerializerMethodField()

    contact_unlock_expires_at = serializers.SerializerMethodField()

    contact_unlock_fee = serializers.SerializerMethodField()

    contact_unlock_payment_status = serializers.SerializerMethodField()

    contact_unlock_rejection_reason = serializers.SerializerMethodField()

    owner_profile_picture = serializers.SerializerMethodField()

    region_name = serializers.SerializerMethodField()

    district_name = serializers.SerializerMethodField()

    ward_name = serializers.SerializerMethodField()

    street_area_name = serializers.SerializerMethodField()

    owner_id_document_url = serializers.SerializerMethodField()

    first_image = serializers.SerializerMethodField()

    images = serializers.SerializerMethodField()

    class Meta:

        model = Listing

        fields = [
            'id',
            'category',
            'category_id',
            'owner',
            'owner_full_name',
            'owner_first_name',
            'owner_last_name',
            'owner_phone_number',
            'can_view_contact',
            'contact_unlock_expires_at',
            'contact_unlock_fee',
            'contact_unlock_payment_status',
            'contact_unlock_rejection_reason',
            'owner_profile_picture',
            'first_image',
            'images',
            'title',
            'description',
            'location',
            'region',
            'region_name',
            'district',
            'district_name',
            'ward',
            'ward_name',
            'street_area',
            'street_area_name',
            'location_description',
            'price',
            'publishing_fee',
            'featured_package',
            'featured_until',
            'payment_status',
            'payment_method',
            'payment_reference',
            'payment_rejection_reason',
            'listing_rejection_reason',
            'owner_id_document_url',
            'availability_status',
            'is_approved',
            'is_featured',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def get_owner_full_name(
        self,
        obj
    ):

        return obj.owner.get_full_name() or obj.owner.username

    def get_region_name(self, obj):

        return obj.region.name if obj.region else ''

    def get_district_name(self, obj):

        return obj.district.name if obj.district else ''

    def get_ward_name(self, obj):

        return obj.ward.name if obj.ward else ''

    def get_street_area_name(self, obj):

        return obj.street_area.name if obj.street_area else ''

    def get_owner_id_document_url(self, obj):

        request = self.context.get(
            'request'
        )

        if not obj.owner_id_document:

            return ''

        url = obj.owner_id_document.url

        if request:

            return request.build_absolute_uri(
                url
            )

        return url

    def get_owner_profile_picture(
        self,
        obj
    ):

        if not obj.owner.profile_picture:

            return None

        request = self.context.get(
            'request'
        )

        if request:

            return request.build_absolute_uri(
                obj.owner.profile_picture.url
            )

        return obj.owner.profile_picture.url

    def _get_active_contact_unlock(
        self,
        obj
    ):

        request = self.context.get(
            'request'
        )

        if not request or not request.user.is_authenticated:

            return None

        if request.user == obj.owner or request.user.is_superuser:

            return None

        return ContactUnlock.objects.filter(
            user=request.user,
            listing=obj,
            is_paid=True,
            expires_at__gt=timezone.now()
        ).first()

    def _get_contact_unlock(self, obj):

        request = self.context.get(
            'request'
        )

        if not request or not request.user.is_authenticated:

            return None

        if request.user == obj.owner or request.user.is_superuser:

            return None

        return ContactUnlock.objects.filter(
            user=request.user,
            listing=obj
        ).first()

    def get_can_view_contact(
        self,
        obj
    ):

        request = self.context.get(
            'request'
        )

        if not request or not request.user.is_authenticated:

            return False

        if request.user == obj.owner or request.user.is_superuser:

            return True

        return self._get_active_contact_unlock(
            obj
        ) is not None

    def get_contact_unlock_expires_at(
        self,
        obj
    ):

        contact_unlock = self._get_active_contact_unlock(
            obj
        )

        if not contact_unlock:

            return None

        return contact_unlock.expires_at

    def get_contact_unlock_fee(
        self,
        obj
    ):

        return settings.CONTACT_UNLOCK_FEE

    def get_contact_unlock_payment_status(
        self,
        obj
    ):

        contact_unlock = self._get_contact_unlock(
            obj
        )

        if not contact_unlock:

            return None

        return contact_unlock.payment_status

    def get_contact_unlock_rejection_reason(
        self,
        obj
    ):

        contact_unlock = self._get_contact_unlock(
            obj
        )

        if not contact_unlock:

            return ''

        return contact_unlock.payment_rejection_reason

    def to_representation(
        self,
        obj
    ):

        data = super().to_representation(
            obj
        )

        request = self.context.get(
            'request'
        )

        if not self.get_can_view_contact(obj):

            data.pop(
                'owner_phone_number',
                None
            )

        can_view_payment = (
            request
            and request.user.is_authenticated
            and (
                request.user == obj.owner
                or request.user.is_superuser
            )
        )

        if not can_view_payment:

            data.pop(
                'publishing_fee',
                None
            )

            data.pop(
                'payment_reference',
                None
            )

            data.pop(
                'payment_method',
                None
            )

            data.pop(
                'payment_rejection_reason',
                None
            )

            data.pop(
                'listing_rejection_reason',
                None
            )

        return data

    def get_first_image(
        self,
        obj
    ):

        request = self.context.get(
            'request'
        )

        image = obj.images.first()

        if image:

            if request:

                return request.build_absolute_uri(
                    image.image.url
                )

            return image.image.url

        return None

    def get_images(
        self,
        obj
    ):

        request = self.context.get(
            'request'
        )

        image_list = []

        for image in obj.images.all():

            if request:

                image_url = request.build_absolute_uri(
                    image.image.url
                )

            else:

                image_url = image.image.url

            image_list.append(

                {
                    'id': image.id,
                    'image': image_url,
                }

            )

        return image_list


# ==========================================================
#            USER REGISTRATION SERIALIZER
# ==========================================================

class UserRegisterSerializer(
    serializers.ModelSerializer
):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'password',
        ]

    def create(
        self,
        validated_data
    ):

        user = User.objects.create_user(

            username=validated_data['username'],

            first_name=validated_data.get(
                'first_name',
                ''
            ),

            last_name=validated_data.get(
                'last_name',
                ''
            ),

            phone_number=validated_data['phone_number'],

            password=validated_data['password']

        )

        return user


# ==========================================================
#            CREATE LISTING SERIALIZER
# ==========================================================

class ListingCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Listing

        fields = [

            'category',

            'title',

            'description',
            'region',
            'district',
            'ward',
            'street_area',
            'location_description',

            'price',
            'owner_id_document',

        ]

    def validate(
        self,
        attrs
    ):

        region = attrs.get(
            'region',
            getattr(self.instance, 'region', None)
        )
        district = attrs.get(
            'district',
            getattr(self.instance, 'district', None)
        )
        ward = attrs.get(
            'ward',
            getattr(self.instance, 'ward', None)
        )
        street_area = attrs.get(
            'street_area',
            getattr(self.instance, 'street_area', None)
        )
        owner_id_document = attrs.get(
            'owner_id_document',
            getattr(self.instance, 'owner_id_document', None)
        )

        errors = {}

        if not region:

            errors['region'] = 'Please choose a region.'

        if not district:

            errors['district'] = 'Please choose a district.'

        elif region and district.region_id != region.id:

            errors['district'] = (
                'Please choose a district in the selected region.'
            )

        if not ward:

            errors['ward'] = 'Please choose a ward.'

        elif district and ward.district_id != district.id:

            errors['ward'] = 'Please choose a ward in the selected district.'

        if not street_area:

            errors['street_area'] = 'Please choose a street or area.'

        elif ward and street_area.ward_id != ward.id:

            errors['street_area'] = (
                'Please choose a street or area in the selected ward.'
            )

        if not owner_id_document:

            errors['owner_id_document'] = (
                'Please upload a photo of your ID before submitting this listing.'
            )

        if errors:

            raise serializers.ValidationError(
                errors
            )

        return attrs

    def validate_owner_id_document(self, value):

        validate_image_upload(
            value
        )

        return value


class ListingPaymentSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Listing

        fields = [
            'featured_package',
            'payment_method',
            'payment_reference',
            'payment_note',
        ]

    def validate(
        self,
        attrs
    ):

        if not attrs.get('featured_package'):

            raise serializers.ValidationError(
                {
                    'featured_package': 'Please choose a featured listing package.'
                }
            )

        if attrs.get('featured_package') not in Listing.FEATURED_PACKAGES:

            raise serializers.ValidationError(
                {
                    'featured_package': 'Please choose a valid featured listing package.'
                }
            )

        if not attrs.get('payment_method'):

            raise serializers.ValidationError(
                {
                    'payment_method': 'Please choose the payment method used.'
                }
            )

        if not PublishingPaymentMethod.objects.filter(
            code=attrs.get('payment_method'),
            is_active=True
        ).exists():

            raise serializers.ValidationError(
                {
                    'payment_method': 'Please choose an active payment method.'
                }
            )

        if not attrs.get('payment_reference'):

            raise serializers.ValidationError(
                {
                    'payment_reference': 'Please enter the payment reference.'
                }
            )

        return attrs


# ==========================================================
#                USER SERIALIZER
# ==========================================================

class UserSerializer(
    serializers.ModelSerializer
):

    profile_picture = serializers.SerializerMethodField()

    class Meta:

        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
            'is_verified',
            'created_at',
        ]

    def get_profile_picture(
        self,
        obj
    ):

        if not obj.profile_picture:

            return None

        request = self.context.get(
            'request'
        )

        if request:

            return request.build_absolute_uri(
                obj.profile_picture.url
            )

        return obj.profile_picture.url

    def to_representation(
        self,
        obj
    ):

        data = super().to_representation(
            obj
        )

        request = self.context.get(
            'request'
        )

        can_view_phone = (
            request
            and request.user.is_authenticated
            and (
                request.user == obj
                or request.user.is_superuser
            )
        )

        if not can_view_phone:

            data.pop(
                'phone_number',
                None
            )

        return data


# ==========================================================
#         LISTING IMAGE CREATE SERIALIZER
# ==========================================================

class ListingImageCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ListingImage

        fields = [
            'image',
        ]

    def validate_image(
        self,
        value
    ):

        validate_image_upload(
            value
        )

        return value


# ==========================================================
#          USER UPDATE SERIALIZER
# ==========================================================

class UserUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
        ]

    def validate_profile_picture(
        self,
        value
    ):

        validate_image_upload(
            value
        )

        return value


# ==========================================================
#       VERIFICATION REQUEST SERIALIZER
# ==========================================================

class VerificationRequestSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = VerificationRequest

        fields = [
            'id',
            'status',
            'id_document',
            'rejection_reason',
            'created_at',
        ]

    def validate_id_document(
        self,
        value
    ):

        validate_image_upload(
            value
        )

        return value
