from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(UserRole)


class SearchShopkeeper(admin.ModelAdmin):
    search_fields = ('user__username',)

admin.site.register(Shopkeeper, SearchShopkeeper)