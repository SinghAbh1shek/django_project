from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_list, name='chat_list'),
    path("<str:username>/", chat_view, name="chat"),
]
