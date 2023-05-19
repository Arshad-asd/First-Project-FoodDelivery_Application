from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import CustomUser
# Register your models here.
class CustomUser(admin.ModelAdmin):
    list_display = ('name','email', 'password','mobile')
admin.site.register(get_user_model())