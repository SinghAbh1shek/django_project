from django.urls import path
from .views import *

urlpatterns = [
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('remove-to-cart/', remove_to_cart, name='remove_to_cart'),
    path('remove-item-from-cart/', remove_item_from_cart, name='remove_item_from_cart'),
    path('clear-cart/', empty_cart, name='clear_cart'),
    path('cart/', get_cart, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('success/', success, name='success'),
    path('order/', orders, name='order'),
    path('order-detail/', order_details, name='order_detail'),
    path('wishlist/', wishlist, name='wishlist'),
    path('add-to-wishlist/', add_to_wishlist, name='add-to-wishlist'),
    path('remove-to-wishlist/', remove_to_wishlist, name='remove-to-wishlist'),
    path('moves-to-wishlist/', moves_to_wishlist, name='moves-to-wishlist'),
    path('generate-invoice/', generate_invoice, name='generate_invoice'),
]
