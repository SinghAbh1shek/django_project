from django.urls import path
from .views import *

urlpatterns = [
    path('', chats, name='chats'),
]
