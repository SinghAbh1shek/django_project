from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def feed(request):
    return render(request, 'posts/feed.html')

@login_required(login_url='login')
def create_post(request):
    return render(request, 'posts/create_post.html')
