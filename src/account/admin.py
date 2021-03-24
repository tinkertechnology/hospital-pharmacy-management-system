from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, PasswordResetOTP
from .models import PhoneOTP, Doctor, Visit, VisitType, BloodGroup, Gender



class AccountAdmin(UserAdmin):
	list_display = ('mobile','username','date_joined', 'firstname', 'lastname', 'email', 'last_login', 'is_admin','is_staff')
	search_fields = ('mobile','username',)
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'mobile', 'email', 'password1', 'password2')}
        ),
    )


admin.site.register(Account, AccountAdmin)
admin.site.register(PhoneOTP)
admin.site.register(PasswordResetOTP)
admin.site.register(Doctor)
admin.site.register(Visit)
admin.site.register(Gender)
admin.site.register(VisitType)
admin.site.register(BloodGroup)



