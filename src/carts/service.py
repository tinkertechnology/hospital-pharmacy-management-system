from .models import Cart, CartItem
def CartItemCreateService(data):
	user_id = data.get('user_id')
	item_id = data.get('item_id')
	quantity = data.get('quantity')
	is_add_sub_qty = data.get('is_add_sub_qty')
	
	cart = Cart.objects.filter(user_id=user_id).filter(active=1).first()
	if cart == None:
		dict_cart = {}
		cart = Cart.objects.create(user_id=user_id,  **dict_cart) 
		cart.active = 1
		cart.tax_percentage = 0.13
		cart.save()

	active_cart_id = cart.id	
	aitem = CartItem.objects.filter(item_id=item_id).filter(cart_id=cart.id).first()

	
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
		"cart_id" : cart.id
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

	return cartItem