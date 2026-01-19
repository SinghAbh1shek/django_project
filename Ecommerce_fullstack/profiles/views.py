from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def profile_page(request):
    return render(request, 'profile.html')

def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').replace(' ', '').lower()
        username = request.POST.get('username', '').replace(' ', '').lower()
        avatar = request.FILES.get('avatar')

        if not username or (not email and not phone):
            print('error: please fill the required field')
            return redirect('edit-profile')
        
        if not '@' in email:
            print('error: enter valid email')
            return redirect('edit-profile')
        
        if phone and (not phone.isdigit() or len(phone) != 10):
            print('error: enter valid phone number')
            return redirect('edit-profile')

        if User.objects.exclude(id = user.id).filter(username=username).exists():
            print('error: username already taken')
            return redirect('edit-profile')

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        customer = user.customer
        customer.phone = phone

        if avatar:
            if customer.avatar:
                customer.avatar.delete(save=False)
            customer.avatar = avatar
            
        customer.save()

            
        
        print('Sucess: user profile edited')
        return redirect('profile')
    return render(request, 'edit_profile.html')
