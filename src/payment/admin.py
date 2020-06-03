from django.contrib import admin

# Register your models here.

from .models import PaymentMethod

admin.site.register(PaymentMethod)
