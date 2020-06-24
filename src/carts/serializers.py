from rest_framework import serializers


from orders.models import UserAddress, UserCheckout
from products.models import Variation
from store.serializers import StoreSerializer

from .models import CartItem, Cart
from products.models import Product,ProductImage
from .mixins import TokenMixin



"""

{
"cart_token": "12345", 
"billing_address": 1,
"shipping_address": 1,
"checkout_token": "12345",
"is_delivered" : 0,
"fk_ordered_store" : 0, 
"fk_delivery_user" : 0,
"is_paid" : 0 , 
"fk_payment_method" : 0
}

"""
class CheckoutSerializer(TokenMixin, serializers.Serializer):
	checkout_token = serializers.CharField()
	billing_address = serializers.IntegerField()
	shipping_address = serializers.IntegerField()
	cart_token = serializers.CharField()
	user_checkout_id =serializers.IntegerField(required=False)
	cart_id = serializers.IntegerField(required=False)

	def validate(self, data):
		checkout_token = data.get("checkout_token")
		billing_address = data.get("billing_address")
		shipping_address = data.get("shipping_address")
		cart_token = data.get("cart_token")

		cart_token_data = self.parse_token(cart_token)
		cart_id = cart_token_data.get("cart_id")
		#print cart_token_data


		checkout_data = self.parse_token(checkout_token)
		user_checkout_id = checkout_data.get("user_checkout_id")
		#print checkout_data


		# try:
		# 	cart_obj = Cart.objects.get(id=int(cart_id))
		# 	data["cart_id"] = cart_obj.id
		# except:
		# 	raise serializers.ValidationError("This is not a valid cart")

		# try:
		# 	user_checkout = UserCheckout.objects.get(id=int(user_checkout_id))
		# 	data["user_checkout_id"] = user_checkout.id
		# except:
		# 	raise serializers.ValidationError("This is not a valid user")


		# try:
		# 	billing_obj = UserAddress.objects.get(user__id=int(user_checkout_id), id=int(billing_address))
		# except:
		# 	raise serializers.ValidationError("This is not a valid address for this user")

		# try:
		# 	shipping_obj = UserAddress.objects.get(user__id=int(user_checkout_id), id=int(shipping_address))
		# except:
		# 	raise serializers.ValidationError("This is not a valid address for this user")

		return data

	# def validate_<fieldname>(self, value):
	#   	return value
	# def validate_checkout_token(self, value):
	# 	print type(value)
	# 	if type(value) == type(str()):
	# 		return value
	# 	raise serializers.ValidationError("This is not a valid token.")



class CartVariationSerializer(serializers.ModelSerializer):
	product = serializers.SerializerMethodField()
	class Meta:
		model = Variation
		fields = [
			"id",
			"title",
			"price",
			"product",
		]

	def get_product(self, obj):
		return obj.product.title

class ProductImageSerializer(serializers.ModelSerializer):
	# image_url = serializers.SerializerMethodField('get_image_url')

	class Meta:
		model = ProductImage
		fields = '__all__'

	



class CartItemSerializer(serializers.ModelSerializer):
	#item = CartVariationSerializer(read_only=True)
	# url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')
	item = serializers.SerializerMethodField()
	product_id = serializers.SerializerMethodField()
	item_title = serializers.SerializerMethodField()
	product = serializers.SerializerMethodField()
	price = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()
	fk_store_title = serializers.SerializerMethodField() #StoreSerializer(read_only=True)


	class Meta:
		model = CartItem
		fields = [
			# "url",
			"product_id",
			"image",
			"item",
			"item_title",
			"price",
			"product",
			"quantity",
			"line_item_total",
			"fk_store_title"
		]

	def get_item(self,obj):
		return obj.item.id

	def get_product_id(self, obj):
		return obj.id
		
	def get_item_title(self, obj):
		return "%s %s" %(obj.item.product.title, obj.item.title)

	def get_product(self, obj):
		return obj.item.product.id

	def get_fk_store_title(self, obj):
		#return  StoreSerializer(obj.item.product.fk_store)
		return obj.item.product.fk_store.title 

	def get_price(self, obj):
		print(obj.item.sale_price)
		print(obj.item.price)
		print(obj.item.id)
		# print(obj.item.sale_price)
		if obj.item.sale_price is None:
			return obj.item.price
		return obj.item.sale_price

	def get_image(self, obj):
		# image_url = ProductImage.objects.filter(product_id=obj.item.id).first()
		variation = obj.item
		product = variation.product

		image_url = ProductImage.objects.filter(product=product).first()
		print(obj.item.id)
		print(obj.__dict__)
		print(image_url)
		# return ""
		# print(list(image_url.values('image')))
		
		imageUrl = "/static/no-image.jpg"
		d = image_url.__dict__
		if 'image' in d:
			imageUrl = d['image']



		# return image_url.image

		return imageUrl


class AddToCartSerializer(serializers.ModelSerializer):
	created_by = serializers.CurrentUserDefault()
	item_quantity = serializers.CharField()


	class Meta:
		model = Cart
		fields = '__all__'


	def create(self, validated_data):
		user =  self.context['request'].user
		print(user)
		item_quantity = validated_data.pop('item_quantity')
		return Cart.objects.create(user_id=user.id, **validated_data)



		

class CartItemModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields ='__all__'


	def create(self, validated_data):
		request = self.context['request']
		print(request.GET.get('is_add_sub_qty'))
		user =  self.context['request'].user
		print(user)
		# item_quantity = validated_data.pop('item_quantity')
		# return Cart.objects.create(user_id=user.id, **validated_data)
		cart = Cart.objects.filter(user_id=user.id).filter(active=1).first()
		# cart_id = cart.id
		# if cart_id == None:

		if cart == None:
			dict_cart = {}
			cart = Cart.objects.create(user_id=user.id,  **dict_cart)
			cart.active = 1
			cart.tax_percentage = 0.13
			cart.save()

		active_cart_id = cart.id
		aitem = CartItem.objects.filter(item_id=validated_data['item']).filter(cart_id=cart.id).first() #CartItem.objects.filter(item_id=validated_data['item'], cart_id=cart.id).first()


		if aitem:		
			quantity = validated_data['quantity']
			is_add_sub_qty = request.GET.get('is_add_sub_qty', None)
			if is_add_sub_qty:
				aitem.quantity = quantity
				aitem.save()
				return aitem

			update_cart_items = quantity + aitem.quantity

			#cartItems = aitem.update(quantity=update_cart_items)
			aitem.quantity = update_cart_items
			aitem.save()
			return aitem
			



		cart_items = {
			"quantity": validated_data['quantity'],
			"item" : validated_data['item'],
			"cart_id" : cart.id
		}

		cartItems= CartItem.objects.create(**cart_items)
			# cart_id = cart.id

			# self.request.session["cart_id"] = cart_id
			# Cart.objects.filter(user_id=self.request.user.id).first().id= cart_id
		# cart_id = cart.id
		# cart = Cart.objects.get(id=cart_id)
		# if self.request.user.is_authenticated:
		# 	cart.user = self.request.user
		# 	cart.save()

		return cartItems



class RemoveCartItemFromCartSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields = '__all__'

	def destroy(self, request, *args, **kwargs):
		try:
			instance = self.get_object()
			self.perform_destroy(instance)
		except Http404:
			pass

		return Response(status=status.HTTP_204_NO_CONTENT)


		# return item 



