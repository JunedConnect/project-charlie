from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User, Profile, Achievement

# Register your models here.



# Inherits Profile info into User Info

class ProfileInLine(admin.StackedInline):

    model = Profile

# Allows Profile fields to be viewed through User page

class CustomUserAdmin(UserAdmin):

    inlines = [ProfileInLine]

# Unregister Groups

admin.site.unregister(Group)

# Register Users

admin.site.register(User, CustomUserAdmin)

# Register Achievements

admin.site.register(Achievement)