from django.contrib import admin

# Register your models here.


from .models import UserCheckout, UserAddress, Order, Quotation


admin.site.register(UserCheckout)


admin.site.register(UserAddress)

admin.site.register(Order)
admin.site.register(Quotation)