from .models import Cart, CartItem
from django.conf import settings
from products.models import Variation
from store.service import UserAccountStoreWiseSaveService
from decimal import Decimal
from orders.service import  VariationHistoryCountService

def CartItemCreateService(data):
	is_auto_order = data.get('is_auto_order', False); #auto order, by customer
	user_id = data.get('user_id')
	item_id = data.get('item_id')
	quantity = data.get('quantity')
	debit = data.get('debit', 0)
	credit = data.get('credit', 0)
	is_add_sub_qty = data.get('is_add_sub_qty')
	print('----')
	print(credit)
	# 2 types of cart:
	# cart with auto_order = True; # every 3 days/ 2 day item are auto ordered
	# auto_order = False; # user selects and adds item to cart	
	cart_query = Cart.objects.filter(user_id=user_id).filter(active=1).filter(is_auto_order=is_auto_order)
	cart = cart_query.first()

	if cart == None:
		dict_cart = {}
		cart = Cart.objects.create(user_id=user_id,  **dict_cart) 
		cart.active = 1
		cart.credit = credit
		cart.debit = debit
		cart.tax_percentage = settings.TAX_PERCENT_DECIMAL#0.13
		cart.is_auto_order = is_auto_order
		cart.save()

	active_cart_id = cart.id	
	aitem = CartItem.objects.filter(item_id=item_id).filter(cart_id=cart.id).first()
	print('aitem')
	# print(aitem.item)
	if aitem:		
		if is_add_sub_qty:
			aitem.quantity = quantity
			aitem.save()
			return aitem
		update_cart_items = quantity + aitem.quantity

		aitem.quantity = update_cart_items
		aitem.save()
		return aitem

	cart_item = {
		"quantity": quantity, 
		#"item" : data.get('item'], 
		"item_id" : item_id, 
		"cart_id" : cart.id,
		# "credit" : credit
	}
	
	cartItem= CartItem.objects.create(**cart_item)
	# cart_id = cart.id


	# self.request.session["cart_id"] = cart_id
	# Cart.objects.filter(user_id=self.request.user.id).first().id= cart_id
	
	# cart_id = cart.id
	# cart = Cart.objects.get(id=cart_id)
	# if self.request.user.is_authenticated:
	# 	cart.user = self.request.user
	# 	cart.save()
	user_account_data = {
			'fk_user_id': user_id,
			'fk_store_id': Variation.objects.get(pk=item_id).product.fk_store.id,
			'credit': (Decimal(cart.total)-Decimal(debit))
		}
	print("user_acc_data",user_account_data)
	UserAccountStoreWiseSaveService(user_account_data)
	print(user_account_data)
	return cartItem



#mistakely ordered in cart
# staff will delete that cart and reorder new cart
def CartItemSoftDelete(data):
	cart_id = data.get('cart_id')
	cart = Cart.objects.filter(pk=cart_id).first()
	cart.isDeleted = true;

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