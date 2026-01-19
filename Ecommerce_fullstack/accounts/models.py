from django.db import models
from django.contrib.auth .models import User
from utils.utility.models import BaseModel

class UserRole(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        if self.is_seller and self.is_customer:
            return f'Seller and Customer'
        elif self.is_customer:
            return f'Customer'
        elif self.is_seller:
            return f'Seller'
        else:
            return 'None'


class BaseProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        abstract = True

class Customer(BaseProfile):
    class Meta:
        db_table = 'Customer'

    def __str__(self):
        return f"customer - {self.user.username}"
    
    def cartItemsCount(self):
        from orders.models import CartItems
        return CartItems.objects.filter(cart__customer = self, cart__is_paid = False).count()
    
    def WishlistItemsCount(self):
        from orders.models import WishlistItems
        return WishlistItems.objects.filter(wishlist__customer = self).count()
    
class Shopkeeper(BaseProfile):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    shop_name = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=15, unique=True)
    adhar_number = models.CharField(max_length=12, unique=True)
    adhar_image = models.ImageField(upload_to='shopkeepers_docs/', null=True, blank=True)
    bmp_id = models.CharField(max_length=100, unique=True)
    verification_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Seller - {self.shop_name}"
