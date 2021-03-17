from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import Profile

"""class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email','username','age',]
admin.site.register(CustomUser,CustomUserAdmin)
"""

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','date_of_birth']
