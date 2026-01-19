from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('search/', search, name='search'),
    path('products/<id>/', product_details, name='products'),
    path('categories/<id>/', categories, name='categories'),
]