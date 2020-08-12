from django.contrib import admin

# Register your models here.


from .models import UserCheckout, UserAddress, Order, Quotation, StoreWiseOrder

list_filter = (['fk_ordered_store'])

admin.site.register(UserCheckout)


admin.site.register(UserAddress)

admin.site.register(Order)
# admin.site.register(Quotation)
admin.site.register(StoreWiseOrder)