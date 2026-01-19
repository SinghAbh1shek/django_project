from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Customer, UserRole
from django.contrib.auth.models import User

import requests
from django.core.files.base import ContentFile
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount

@receiver(post_save, sender=User)
def customer_post_save(sender, instance, created, **kwargs):
    if created:
        Customer.objects.get_or_create(user = instance)
        UserRole.objects.get_or_create(user = instance)

@receiver(user_signed_up)
def save_google_profile_image(request, user, **kwargs):
    try:
        social_account = SocialAccount.objects.get(user = user, provider = 'google')

    except SocialAccount.DoesNotExist:
        return
    
    data = social_account.extra_data

    picture_url = data.get('picture')

    if not picture_url: 
        return
    
    customer, _ = Customer.objects.get_or_create(user = user)
    if customer.avatar:
        return
    
    try:
        response = requests.get(picture_url, timeout=10)
        if response.status_code == 200:
            customer.avatar.save(
                f"{user.username}_google.jpg",
                ContentFile(response.content),
                save = True
            )
    except Exception as e:
        print('Google image fetched failed: ', e)


@receiver(post_delete, sender=Customer)
def delete_customer_avatar(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.delete(save=False)