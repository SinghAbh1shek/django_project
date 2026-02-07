from django.shortcuts import render, redirect
from .llm import llm
from .models import ChatMessage, Chat
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
    if request.user.is_authenticated:
        user = request.user
        chat_id = request.GET.get('chat_id')
        chat = None
        if chat_id:
            chat = Chat.objects.filter(id = chat_id, user = user).first()

        if request.method == "POST":
            query = request.POST.get("query")
            if not chat:
                chat = Chat.objects.create(user = user, title = query[:30])

            ChatMessage.objects.create(
                chat = chat,
                role="user",
                content=query
            )

            ai_response = llm(query, chat)

            return JsonResponse({
                "assistant": ai_response,
                "chat_id":  chat.id,
                "chat_title": chat.title
                })

        chat_history = ChatMessage.objects.filter(
            chat=chat
        ).order_by("created_at")

        return render(request, "home.html", {
            "chat_history": chat_history
        })
    else:
        if "chat_history" not in request.session:
            request.session["chat_history"] = []

        if request.method == "POST":
            query = request.POST.get("query")

            chat = request.session["chat_history"]
            chat.append({"role": "user", "content": query})

            ai_response = llm(query)
            chat.append({"role": "assistant", "content": ai_response})

            request.session["chat_history"] = chat

            return JsonResponse({"assistant": ai_response})

        return render(request, "home.html")

@login_required
def delete_chat(request, chat_id):
    user = request.user
    try:
        chat = Chat.objects.filter(id = chat_id, user = user).delete()
        return redirect('home')
    except Exception as e:
        print('something goes wrong')
        return redirect('home')

@login_required
def logout_page(request):
    logout(request)
    return redirect('home')