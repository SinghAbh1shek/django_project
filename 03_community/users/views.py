from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def profile(requests):
    return render(requests, 'users/profile.html')

def login_page(request):
    return render(request, 'users/login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not first_name or last_name or username or email or password:
            messages.error(request, "Note: All fields marked with * are required")
            return redirect('register')

        print(first_name)
        print(last_name)
        print(username)
        print(email)
        print(password)
        messages.success(request, "account created")
        return redirect('register')
    return render(request, 'users/register.html')
