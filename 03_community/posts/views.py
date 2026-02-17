from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def feed(request):
    return render(request, 'posts/feed.html')
