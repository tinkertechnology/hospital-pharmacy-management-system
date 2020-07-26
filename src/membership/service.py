from .models import UserMembershipAutoOrder
from carts.service import CartItemCreateService
from orders.service import CreateOrderFromCart

#todo: add auto_order_date in cart_item
#so we wont order same item again today, even if this func is run twice
def StartUserMembershipAutoOrder():
	um_auto_orders = UserMembershipAutoOrder.objects.all()
	for um_auto_order in um_auto_orders:
		#print(um_auto_order)
		user_id = um_auto_order.fk_usermembership.fk_member_user_id
		data = {
			'user_id': user_id,
			'item_id': um_auto_order.fk_variation_id,
			'quantity': um_auto_order.quantity,
			'is_auto_order': True
		}
		print(data)
		CartItemCreateService(data)

		#todo: add payment type in membership
		order_data = {
			'user_id': user_id,
			'order_latitude': 1,
			'order_longitude': 1,
			'is_auto_order': True,
			'fk_payment_method': 1
		}
		print( order_data )
		CreateOrderFromCart( order_data )
		pass
	return