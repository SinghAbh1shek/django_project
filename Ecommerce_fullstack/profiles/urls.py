from django.urls import path
from .views import *

urlpatterns = [
    path('', profile_page, name='profile'),
    path('edit-profile/', edit_profile, name='edit-profile'),
]