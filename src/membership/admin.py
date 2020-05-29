from django.contrib import admin

# Register your models here.

from .models import MembershipType,UserMembership 

admin.site.register(MembershipType)
admin.site.register(UserMembership)