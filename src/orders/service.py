from rest_framework import serializers
from rest_framework.exceptions import APIException

from carts.mixins import TokenMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import  Order, StoreWiseOrder

from products.models import Product, ProductImage, UserVariationQuantityHistory
from carts.models import Cart, CartItem
from store.models import Store
from store.serializers import StoreWiseOrderSerializer, StoreSerializer
import pprint
from django.contrib.auth import get_user_model
from django.conf import settings
from decimal import Decimal
User = get_user_model()


# sign: default 1, pass -1 to decreament ordered_items (if cart is deleted)
def VariationHistoryCountService(data):
	cart_id = data.get('cart_id')
	sign = data.get('sign', 1)
	# comment = data.get('comment')
	storewiseorder = StoreWiseOrder.objects.filter(cart_id=cart_id).first()
	ordered_by_user = storewiseorder.fk_auth_user
	ordered_items = storewiseorder.cart.cartitem_set.all()
	for item in ordered_items:
		var_history = UserVariationQuantityHistory.objects.filter(variation=item.item).filter(user=ordered_by_user).first() #item is cartitem instance and .item is variation instance
		if not var_history:
			var_history = UserVariationQuantityHistory()
		if item.item.is_refill: #refill true ho bhane + jodixa
			var_history.num_taken +=float(item.quantity)
			var_history.num_delta +=float(item.quantity)  #var_history.num_taken - var_history.num_returned
			var_history.variation = item.item
			var_history.user = ordered_by_user
			# if comment:
			# 	var_history.comment += comment
			var_history.save()
		

# maybe save flag to retn jar in storewise order (single row)

# import uservariation history
#
# forloop get variation, qty of each items in storewise_orders
# 	var_history = new/edit existing history for user, variation
# 	var_history.firta_garne_qty += qty
# 	var_history.variation = varition
# 	
# 	Variation: jar firta yes/no bhanne flag, 140ko ma firta qty add huncha arko ma hunna
	
# # Firta garne form/api
#  phone no customer:
#  variation: 
#  qty_returned: 

def SaveStoreWiseOrder(order, user_id):
	print('order::')
	print(order.__dict__)
	cart = order.cart
	cart_items = cart.items
	cart_items = CartItem.objects.filter(cart_id=cart.id)
	ordered_by = Store.objects.filter(fk_user_id=user_id).first()
	#ordered_by_store = ordered_by.id
	#print(ordered_by_store)

	# print('asdasdasdasd')
	for variation in cart_items:
		print(variation)
		store = variation.item.product.fk_store
		pprint.pprint(['store=', store, 'variation==', variation.item])
		order_id = order.id
		
		store_id = store.id
		pprint.pprint(['order_id=', order_id, 'store_id==', store_id])
		store_wise = StoreWiseOrder.objects.filter(order_id=order_id).filter(fk_ordered_store_id=store_id).all().first()

		pprint.pprint(['storewise=', store_wise])
		if store_wise is None:			
			store_wise = StoreWiseOrder()
			#store_wise.save() #StoreWiseOrder()
		store_wise.order_id = order.id

		store_wise.order_total = order.order_total
		
		# pprint.pprint(['tax-am', store_wise.order_total, store_wise.tax_amount,  Decimal(settings.TAX_PERCENT_DECIMAL), store_wise.grand_total_amount] )

		store_wise.billing_address = order.billing_address
		store_wise.shipping_address = order.shipping_address
		store_wise.user_id = order.user_id
		store_wise.cart_id = order.cart_id
		store_wise.fk_auth_user_id = order.fk_auth_user_id
		store_wise.order_latitude = order.order_latitude
		store_wise.order_longitude = order.order_longitude
		store_wise.fk_ordered_store = store
		store_wise.fk_delivery_user_id = order.fk_delivery_user_id
		store_wise.fk_ordered_by_store = ordered_by
		store_wise.fk_payment_method = order.fk_payment_method
		store_wise.is_auto_order = order.is_auto_order
		if order.is_delivered:
			store_wise.is_delivered = order.is_delivered
		store_wise.save()
		variation.fk_storewise_order_id = store_wise.id
		variation.save()

	store_wise_orders = StoreWiseOrder.objects.filter(order_id=order.id) 
	print('store-wise-order')
	print(store_wise_orders)
	for store_wise_order in store_wise_orders:
		sw_cart_items =  CartItem.objects.filter(fk_storewise_order_id=store_wise_order.id) #store_wise_order.fk_storewise_order_id
		store_wise_order.order_total = 0
		if store_wise_order.order_latitude and store_wise_order.order_longitude:
			store_wise_order.fk_route = get_nearest_route(
				store_wise_order.order_latitude,
				store_wise_order.order_longitude,
				store_wise_order.fk_ordered_store.id,
				None
			)

		print(store_wise_order.fk_route)
		for cart_item in sw_cart_items:
			store_wise_order.order_total+=cart_item.line_item_total
		store_wise_order.tax_amount = Decimal(float(store_wise_order.order_total) * settings.TAX_PERCENT_DECIMAL) ##tax jodeko calculation
		store_wise_order.grand_total_amount = store_wise_order.order_total + store_wise_order.tax_amount
		store_wise_order.save()


		# print(variation.product)

# used from
# /api/create_order/ #CartOrderApiView(CreateAPIView): #CartOrderSerializer(serializers.ModelSerializer):
# 
def CreateOrderFromCart(validated_data):
	#pprint.pprint(self.context['request'].__dict__)
	# pprint.pprint(validated_data)
	##user =  self.context['request'].user ##
	##print(user.id)##

	is_auto_order = validated_data.get('is_auto_order', False); #auto order, by customer
	user_id = validated_data.get('user_id')
	user = User.objects.get(pk=user_id)
	order_latitude = validated_data.get("order_latitude")
	order_longitude = validated_data.get("order_longitude")
	fk_payment_method = validated_data.get("fk_payment_method")
	fk_payment_method_id = fk_payment_method
	is_delivered = validated_data.get("is_delivered", False)
	fk_delivery_user_id = validated_data.get('fk_delivery_user_id', None)
	if not isinstance(fk_payment_method_id, int):
		fk_payment_method_id = fk_payment_method.id
	# fk_ordered_store = None
	# if is_auto_order == False: # 
	# 	fk_ordered_store  = validated_data.get("fk_ordered_store")
	# 	fk_ordered_store_id = fk_ordered_store 
	# 	if not isinstance(fk_ordered_store, int):
	# 		fk_ordered_store_id = fk_ordered_store.id

	# todo: check for depo to company order
	# client to depo order both should be preasent
	#if not (order_latitude and order_longitude):
		#raise serializers.ValidationError({"message": "No order_latitude and order_longitude" })
		#raise APIException({"message": "No order_latitude and order_longitude" }) # provide custom key, 500 error i.e. server error
		#raise serializers.ValidationError("No lat and lng") # ok, returns json if called from api View ??? , 400 error i.e. client side 
		#raise APIException("No order_latitude and order_longitude" ) # returns in detail key

	# item_quantity = validated_data.pop('item_quantity')
	cart = Cart.objects.filter(user_id=user_id).filter(active=1).filter(is_auto_order=is_auto_order).first()

	if cart is None:
		raise serializers.ValidationError("This is not a valid cart, first make cart, /api/cart/ or add item to cart ")
	usercheckout_user = UserCheckout.objects.filter(user_id=user_id).first()
	if usercheckout_user is None:
		usercheckout_user = UserCheckout()
		usercheckout_user.user_id = user.id
		usercheckout_user.email = user.email
		usercheckout_user.braintree_id = '0'

		usercheckout_user.save()

	useraddress = UserAddress.objects.filter(user_id=usercheckout_user.id).first()
	if useraddress is None:
		useraddress = UserAddress()
		useraddress.user_id = usercheckout_user.id
		useraddress.save()

	order = Order()
	order.order_id = cart.id
	order.status = 1
	order.shipping_total_price = settings.SHIPPING_PRICE
	order.order_total = cart.total
	order.billing_address = useraddress
	order.shipping_address = useraddress
	order.user_id = usercheckout_user.id
	order.cart_id = cart.id
	order.fk_auth_user_id = user_id
	order.fk_delivery_user_id = fk_delivery_user_id
	order.order_latitude = order_latitude
	order.order_longitude = order_longitude
	if is_delivered:
		order.is_delivered = is_delivered
	# if is_auto_order == False:
	# 	order.fk_ordered_store_id = fk_ordered_store_id #not required  #also, auto order wont supply ordered_store

	order.fk_payment_method_id = fk_payment_method_id #eg: assign id directly
	order.is_auto_order = is_auto_order
	#order.fk_payment_method = validated_data.get("fk_payment_method") #eg: assign model obj

	print(order.__dict__)
	order.save()

	cart.active=0 #(COMMENT TO DEBUG / and prevent MULTIPLE boring ORDER to add to cart)
	cart.save()
	print(settings.IS_MULTI_VENDOR)
	if settings.IS_MULTI_VENDOR:
		SaveStoreWiseOrder(order, user_id)

	return order

