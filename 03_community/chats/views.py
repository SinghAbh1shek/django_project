# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


@login_required(login_url="login")
def chat_list(request):
    conversations = (
        Message.objects
        .filter(Q(sender=request.user) | Q(receiver=request.user))
        .order_by("-timestamp")
    )

    users = {}
    for msg in conversations:
        other = msg.sender if msg.sender != request.user else msg.receiver

        if other.id not in users:
            unread_count = Message.objects.filter(
                sender=other,
                receiver=request.user,
                is_read=False
            ).count()

            users[other.id] = {
                "user": other,
                "unread": unread_count,
            }

    return render(request, "chats/chat_list.html", {
        "chat_users": users.values()
    })


@login_required(login_url="login")
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    )
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    last_message = messages.last()

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect("chat", username=username)

    return render(request, "chats/chat.html", {
        "other_user": other_user,
        "messages": messages,
        "last_message": last_message,
    })