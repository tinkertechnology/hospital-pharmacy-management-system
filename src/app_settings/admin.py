from django.contrib import admin

# Register your models here.

from app_settings.models import AppSettings


admin.site.register(AppSettings)