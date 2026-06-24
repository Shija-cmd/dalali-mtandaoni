from rest_framework import serializers

from .models import (
    Category,
    Listing,
    ListingImage,
    VerificationRequest,
)

from accounts.models import User


# ==========================================================
#                 CATEGORY SERIALIZER
# ==========================================================

class CategorySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Category

        fields = '__all__'


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

    owner_profile_picture = serializers.SerializerMethodField()

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
            'owner_profile_picture',
            'first_image',
            'images',
            'title',
            'description',
            'location',
            'price',
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

            'location',

            'price',

        ]


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
            'created_at',
        ]
