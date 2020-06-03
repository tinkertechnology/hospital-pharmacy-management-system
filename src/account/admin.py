from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
from .models import PhoneOTP



class AccountAdmin(UserAdmin):
	list_display = ('mobile','username','date_joined', 'last_login', 'is_admin','is_staff')
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



