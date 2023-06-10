from django.contrib import admin
from django.contrib.auth.models import User
from Accounts.models import Profile
from rest_framework.authtoken.models import Token

# Register your models here.
admin.site.register(Profile)

from rest_framework.authtoken.models import Token
@admin.register(Token)
class Token_admin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'get_username', 'key', 'created')

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email
    
    get_username.short_description = 'Username'
    get_email.short_description = 'Email'
