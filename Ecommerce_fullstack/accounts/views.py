from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Customer
from django.db import transaction

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email_phone = request.POST.get('email_phone', '').replace(' ', '').lower()
        password = request.POST.get('password')
        
        if not email_phone or not password:
            print('error: all fields are required')
            return redirect('login')
        
        if '@' in email_phone:
            is_email = True
        elif email_phone.isdigit() and len(email_phone) == 10:
            is_email = False
        else:
            print('error: invalid input')
            return redirect('login')
        
        if is_email:
            user_obj = User.objects.filter(email = email_phone).first()
            if not user_obj:
                print('error: email not exist')
                return redirect('login')
            username = user_obj.username
        else:
            customer = Customer.objects.filter(phone=email_phone).first()
            if not customer:
                print('error: phone number not exist')
                return redirect('login')
            username = customer.user.username

        user = authenticate(request, username=username, password=password)
        if not user:
            print('error: invalid credentials')
            return redirect('login')
        
        login(request, user)
        return redirect('home')


    return render(request, 'login.html')

def registration(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_phone = request.POST.get('email_phone', '').replace(' ', '').lower()
        password = request.POST.get('password')
        passwordConfirmation = request.POST.get('passwordConfirmation')

        if not email_phone or not password or not passwordConfirmation:
            print('error: all fields required')
            return redirect('register')

        if password != passwordConfirmation:
            print('error: password mismatched')
            return redirect('register')
        
        if '@' in email_phone:
            is_email = True
        elif email_phone.isdigit() and len(email_phone) == 10:
            is_email = False
        else:
            print('error: invalid input')
            return redirect('register')
        
        if User.objects.filter(username = email_phone).exists():
            print('error: email or phone already exist')
            return redirect('register')
        
        if is_email and User.objects.filter(email = email_phone).exists():
            print('error: email already exist')
            return redirect('register')
        
        if not is_email and Customer.objects.filter(phone = email_phone).exists():
            print('error: phone already exist')
            return redirect('register')
        
        with transaction.atomic():
            if is_email:
                user = User.objects.create_user(
                    username=email_phone,
                    first_name = first_name,
                    last_name = last_name,
                    email = email_phone,
                    password = password,
                )
            else:
                user = User.objects.create_user(
                    username=email_phone,
                    first_name = first_name,
                    last_name = last_name,
                    password = password,
                )
                user.customer.phone = email_phone
                user.customer.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


    return render(request, 'registration.html')

def logout_page(request):
    logout(request)
    print('success: logged out')
    return redirect('login')

