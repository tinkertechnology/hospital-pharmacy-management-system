from django.contrib import admin


# Register your models here.

from .models import UserType, UserTypes
# from .models import User

admin.site.register(UserType)

admin.site.register(UserTypes)



# admin.site.register(User)