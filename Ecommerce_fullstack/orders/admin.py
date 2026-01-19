from django.contrib import admin
from .models import *


admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Wishlist)
admin.site.register(WishlistItems)
admin.site.register(Order)
admin.site.register(OrderItems)
