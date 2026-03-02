from django.contrib.auth import get_user_model

def members_list(request):
    User = get_user_model()
    return {
        "members": User.objects.all()
    }