from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

# from orders.models import UserAddress, UserCheckout
from products.models import Variation
from store.serializers import StoreSerializer

from .models import CartItem, Cart, Comment
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


class CommentSerializer(serializers.ModelSerializer):
	created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
	class Meta:
		model = Comment
		fields = ['comment', 'created_at', 'updated_at']

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

	


from products.serializers import VariationSerializer
class CartItemSerializer(serializers.ModelSerializer):
	#item = CartVariationSerializer(read_only=True)
	# url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')
	item = serializers.SerializerMethodField()
	# variation = serializers.SerializerMethodField()
	product_id = serializers.SerializerMethodField()
	item_title = serializers.SerializerMethodField()
	product = serializers.SerializerMethodField()
	price = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()
	stock_quantity = serializers.SerializerMethodField()
	# fk_store_title = serializers.SerializerMethodField() #StoreSerializer(read_only=True)
	class Meta:
		model = CartItem
		fields = [
			# "url",
			"id",
			"product_id",
			"image",
			"item",
			"item_title",
			"price",
			"product",
			"quantity",
			"line_item_total",
			"stock_quantity"
			# "fk_store_title",
			# "variation"
		]

	# def get_variation(self, obj):
	# 	return VariationSerializer(obj.item).data

	def get_item(self,obj):
		return obj.fk_variation_batch.id
	def get_stock_quantity(self, obj):
		stock = 0
		var_batch = obj.fk_variation_batch
		if var_batch:
			stock = var_batch.quantity
		return stock

	def get_product_id(self, obj):
		# return obj.item.product.id
		print('obj', obj)
		return obj.fk_variation_batch.id
		
	def get_item_title(self, obj):
		return "%s (%s)" %(obj.fk_variation_batch.fk_variation.title, obj.fk_variation_batch.batchno)

	def get_product(self, obj):
		return obj.fk_variation_batch.fk_variation.id

	# def get_fk_store_title(self, obj):
	# 	title=""
	# 	if obj.item.product.fk_store:
	# 		title = obj.item.product.fk_store.title 
	# 	#return  StoreSerializer(obj.item.product.fk_store)
	# 	return title

	def get_price(self, obj):
		# print(obj.item.sale_price)
		# print(obj.item.price)
		# print(obj.item.id)
		# print(obj.item.sale_price)
		# if obj.item.sale_price is None:
		# 	return obj.item.price
		# return obj.item.sale_price
		if obj.fk_variation_batch.sale_price is None:
			return obj.fk_variation_batch.price
		return obj.fk_variation_batch.sale_price

	def get_image(self, obj):
		# image_url = ProductImage.objects.filter(product_id=obj.item.id).first()
		variation = obj.fk_variation_batch.fk_variation
		product = variation.product

		image_url = ProductImage.objects.filter(product=product).first()
		# return ""
		# print(list(image_url.values('image')))
		
		imageUrl = "/static/no-image.jpg"
		if image_url:
			d = image_url.__dict__
		
			if 'image' in d:
				imageUrl = d['image']



		# return image_url.image

		return imageUrl
# from account.serializer import UserSerializer



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



		
from . import service as CartService
class CartItemModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields ='__all__'

	def create(self, validated_data):
		request = self.context['request']
		# print(request.data)
		user =  self.context['request'].user
		# print(validated_data)
		data = {}
		# print('cart-id',request.data.get('cart_id'))
		data['user_id'] = request.data.get('p_id')
		data['fk_visit_id'] = request.data.get('fk_visit_id')
		data['fk_bill_created_user_id'] = user.id
		# data['item_id'] = validated_data.get('item').id
		data['fk_variation_batch_id'] = request.data.get('fk_variation_batch_id')
		data['quantity'] = validated_data['quantity']
		data['is_add_sub_qty'] = request.GET.get('is_add_sub_qty', None)
		data['cart_id'] = request.data.get('cart_id')
		data['cartitem_id'] = request.data.get('cartitem_id')
		data['amount'] = request.data.get('amount') #for transaction table default = 0
		data['comment'] = request.data.get('comment') # if remarks added
		data['fk_type_id'] = request.data.get('fk_type_id') #transaction types like refund deposit etc
		cartItem = CartService.CartItemCreateService(data)
		print(cartItem.__dict__)
		# transaction = {
		# 	"fk_cart_id" : cartItem.cart_id,
		# 	"amount" :  cartItem.ordered_price,#request.data.get('amount'),
		# 	"comment" : request.data.get('comment'),
		# 	"fk_type_id" : request.data.get('fk_type_id')
		# }
		# transaction= Transaction.objects.create(**transaction)
		return cartItem


class CartSeriailzer(serializers.ModelSerializer):
	# user = UserSerializer()
	cart_item = serializers.SerializerMethodField()
	user = serializers.SerializerMethodField()
	class Meta:
		model = Cart
		fields = '__all__'
	
	def get_cart_item(self, obj):
		cart_item = obj.cartitem_set.all()
		ct = CartItemModelSerializer(cart_item, many=True)
		return ct.data
	def get_user(self, obj):
		from account.serializer import UserSerializer
		user = UserSerializer(User.objects.filter(pk=obj.user.id).first())
		return user.data

class RemoveCartItemFromCartSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields = '__all__'

	def destroy(self, request, *args, **kwargs):
		try:
			instance = self.get_object()
			quantity = instance.quantity
			var_batch = instance.fk_variation_batch
			if var_batch:
				var_batch.quantity += quantity
				var_batch.save()
			self.perform_destroy(instance)
		except Http404:
			pass

		return Response(status=status.HTTP_204_NO_CONTENT)


		# return item 


from .models import Transaction
class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = '__all__'
