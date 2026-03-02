from django.urls import path
from .views import *

urlpatterns = [
    path('', feed, name='feed'),
    path('create-post/', create_post, name='create_post'),
]
