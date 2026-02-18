from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()

@login_required(login_url='login')
def profile(requests):
    return render(requests, 'users/profile.html')

def login_page(request):
    return render(request, 'users/login.html')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        profile = request.FILES.get('pfp')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')


        if not first_name or not last_name or not username or not email or not password:
            messages.error(request, "Note: All fields marked with * are required")
            return redirect('register')
        
        if User.objects.filter(username = username).exists() or User.objects.filter(email = email).exists():
            messages.error(request, "Note: username or email already exist")
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            first_name = first_name,
            last_name = last_name,
            email=email,
            password=password
        )
        if profile:
            user.profile = profile
            user.save()

        user_obj = authenticate(request, username = username, password = password)
        if user_obj:
            login(request, user_obj)
            messages.success(request, "account created")
            return redirect('feed')
        
        messages.error(request, "something goes wrong")
        return redirect('register')

    return render(request, 'users/register.html')

def logout_user(request):
    logout(request)
    return redirect('login')