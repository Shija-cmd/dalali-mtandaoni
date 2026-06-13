from django.contrib import admin
from .models import Favorite

from .models import (
    Category,
    Listing,
    ListingImage
)

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(ListingImage)
admin.site.register(Favorite)