from django.contrib import admin
from .models import UserProfile, BuyerProfile, SellerProfile

admin.site.register(UserProfile)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
