from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product

class UserProfile(models.Model):
    # OneToOneField creates a unique relationship with Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Basic profile fields
    
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"

    def delete(self, *args, **kwargs):
        #get reference to user before deleting
        user=self.user
        #delete the user profile
        super().delete(*args, **kwargs)
        #delete the user
        user.delete()

class BuyerProfile(models.Model):
    # Link to UserProfile
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    # Buyer-specific fields
    shipping_address = models.TextField(blank=True)
    preferred_payment_method = models.CharField(max_length=50, blank=True)
    purchase_history_count = models.IntegerField(default=0)
    buyer_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user_profile.user.username}"

class SellerProfile(models.Model):
    # Link to UserProfile
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    # Seller-specific fields
    seller_account_id= models.CharField(max_length=10, unique=True, blank=True)
    business_name = models.CharField(max_length=100, blank=True)
    business_address = models.TextField(blank=True)
    business_description = models.TextField(blank=True)
    seller_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_sales = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user_profile.user.username}"

    def save(self, *args, **kwargs):
        if not self.seller_account_id:
            # Generate unique seller ID (S + 6 digits)
            last_seller = SellerProfile.objects.all().order_by('-id').first()
            if last_seller:
                last_id = int(last_seller.seller_account_id[1:])
                self.seller_account_id = f'S{str(last_id + 1).zfill(6)}'
            else:
                self.seller_account_id = 'S000001'
        super().save(*args, **kwargs)


# Signal to create UserProfile and BuyerProfile automatically when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       UserProfile.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class UserCart(models.Model):
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"