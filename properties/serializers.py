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

    first_image = serializers.SerializerMethodField()

    images = serializers.SerializerMethodField()

    class Meta:

        model = Listing

        fields = [
            'id',
            'category',
            'category_id',
            'owner',
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
            'phone_number',
            'password',
        ]

    def create(
        self,
        validated_data
    ):

        user = User.objects.create_user(

            username=validated_data['username'],

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

    class Meta:

        model = User

        fields = [
            'id',
            'username',
            'phone_number',
            'is_verified',
            'created_at',
        ]


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
            'phone_number',
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
            'created_at',
        ]