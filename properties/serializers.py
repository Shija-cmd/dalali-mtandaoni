from rest_framework import serializers

from .models import (
    Category,
    Listing,
    ListingImage,
    VerificationRequest,
    )

class CategorySerializer(
    serializers.ModelSerializer
    ):
    class Meta:

        model = Category

        fields = '__all__'
        

class ListingImageSerializer(
    serializers.ModelSerializer
    ):

    class Meta:

        model = ListingImage

        fields = [
            'id',
            'image',
        ]

class ListingSerializer(
    serializers.ModelSerializer
    ):

    category = serializers.StringRelatedField()

    owner = serializers.StringRelatedField()

    first_image = serializers.SerializerMethodField()
    
    images = ListingImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Listing

        fields = '__all__'

    def get_first_image(
        self,
        obj
    ):

        image = obj.images.first()

        if image:

            return image.image.url

        return None
    

from accounts.models import User


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
        
        
class ListingImageCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ListingImage

        fields = [
            'image',
        ]
        
class UserUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = User

        fields = [
            'username',
            'phone_number',
        ]
        
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