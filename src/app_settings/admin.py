from django.contrib import admin

# Register your models here.

from app_settings.models import AppSettings, SideMenu, FiscalYear


admin.site.register(AppSettings)
admin.site.register(SideMenu)
admin.site.register(FiscalYear)
