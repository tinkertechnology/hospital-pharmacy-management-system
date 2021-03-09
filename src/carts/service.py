from .models import Cart, CartItem
from django.conf import settings
from products.models import Variation
# from store.service import UserAccountStoreWiseSaveService
from decimal import Decimal
from orders.service import  VariationHistoryCountService
from products.models import VariationBatch

def CartItemCreateService(data):
	is_auto_order = data.get('is_auto_order', False); #auto order, by customer
	user_id = data.get('user_id')
	cart_id = data.get('cart_id')
	# item_id = data.get('item_id')
	fk_variation_batch_id = data.get('fk_variation_batch_id')
	fk_visit_id = data.get('fk_visit_id')
	quantity = data.get('quantity')
	fk_counter_id = data.get('fk_counter_id')
	print(data)
	cartitem_id = data.get('cartitem_id')
	print('cartitem_id',cartitem_id)
	debit = data.get('debit', 0)
	is_return = data.get('is_return')
	credit = data.get('credit', 0)
	fk_bill_created_user_id = data.get('fk_bill_created_user_id')
	fk_delivery_user_id = data.get('fk_delivery_user_id', None)
	ordered_price = data.get('ordered_price', 0)
	is_add_sub_qty = data.get('is_add_sub_qty')
	# 2 types of cart:
	# cart with auto_order = True; # every 3 days/ 2 day item are auto ordered
	# auto_order = False; # user selects and adds item to cart	
	# cart_query = Cart.objects.filter(user_id=user_id).filter(active=1).filter(is_auto_order=is_auto_order)
	cart_query = Cart.objects.filter(pk=cart_id)#.filter(active=1).filter(is_auto_order=is_auto_order)
	# cart_query = 
	cart = cart_query.first()
	# print('cart_id', cart_id)
	if cart == None:
		dict_cart = {}
		cart = Cart.objects.create(user_id=user_id,  **dict_cart) 
		cart.active = 1
		cart.fk_visit_id = fk_visit_id
		cart.credit = credit
		cart.debit = debit
		cart.fk_bill_created_user_id = fk_bill_created_user_id
		cart.fk_delivery_user_id_id = fk_delivery_user_id
		cart.tax_percentage = settings.TAX_PERCENT_DECIMAL#0.13
		cart.is_auto_order = is_auto_order
		cart.fk_counter_id = fk_counter_id
		cart.save()

	active_cart_id = cart.id
	if cartitem_id:
		print('yei chireko cha')
		cartItem = CartItem.objects.filter(pk=cartitem_id).first() #.filter(cart_id=cart.id).first()
		old_quantity = cartItem.quantity
		cartItem.quantity = quantity
		# aitem.item_id = item_id
		cartItem.fk_variation_batch_id = fk_variation_batch_id
		cartItem.is_return = is_return
		cartItem.save()

		# return aitem
	else:
		old_quantity = 0
		cart_item = {
			"quantity": quantity, 
			#"item" : data.get('item'], 
			"fk_variation_batch_id" : fk_variation_batch_id, 
			"cart_id" : cart.id,
			"ordered_price" : ordered_price
			# "credit" : credit
		}
		
		cartItem= CartItem.objects.create(**cart_item)
		cart_saved = Cart.objects.filter(pk=cart.id).first() #Signal le garda hamle jadu gareko
		if cart_saved.is_auto_order==True: #AutoOrder bhaye matrai credit save garne 
			UserAccountStoreWiseSaveService(user_account_data)
		# print(user_account_data)
	variation_batch = VariationBatch.objects.filter(id=cartItem.fk_variation_batch_id).first()
	if variation_batch:
		if variation_batch.use_batch:
			variation_batch.quantity -= (quantity - old_quantity)
			variation_batch.save()
	return cartItem



#mistakely ordered in cart
# staff will delete that cart and reorder new cart
def CartItemSoftDelete(data):
	cart_id = data.get('cart_id')
	cart = Cart.objects.filter(pk=cart_id).first()
	cart.isDeleted = true

	# decrease credit from deleted cart
	user_account_data = {
			'fk_user_id': user_id,
			'fk_store_id': Variation.objects.get(pk=item_id).product.fk_store.id,
			'credit': (Decimal(cart.total)-Decimal(debit))
		}
	print("user_acc_data",user_account_data)
	UserAccountStoreWiseSaveService(user_account_data)

	# decrease jar from deleted cart
	VariationHistoryCountService(cart_id, -1)