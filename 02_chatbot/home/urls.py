from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='home'),
    path('delete-chat/<chat_id>/', delete_chat, name='delete-chat'),
    path('logout/', logout_page, name='logout'),
]
