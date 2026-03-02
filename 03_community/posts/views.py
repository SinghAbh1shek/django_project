from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from django.contrib import messages

@login_required(login_url='login')
def feed(request):
    posts = Post.objects.all()
    return render(request, 'posts/feed.html', {'posts': posts})

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image', None)

        Post.objects.create(user = request.user, title=title, description=description, image=image)
        

        return redirect('feed')
    return render(request, 'posts/create_post.html')
