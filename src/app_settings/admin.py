from django.contrib import admin

# Register your models here.

from app_settings.models import AppSettings, SideMenu


admin.site.register(AppSettings)
admin.site.register(SideMenu)
