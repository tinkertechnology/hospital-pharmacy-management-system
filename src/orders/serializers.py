from rest_framework import serializers

from carts.mixins import TokenMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import UserAddress, Order, Quotation, UserCheckout, StoreWiseOrder

from products.models import Product, ProductImage
from carts.models import Cart, CartItem
from store.models import Store
from store.serializers import StoreWiseOrderSerializer, StoreSerializer
import pprint
from django.contrib.auth import get_user_model
from django.conf import settings
from routes.models import get_nearest_route
from mysite.utils import jwt_response_payload_handler
User = get_user_model()

# parse order token
# check order not complete
# nonce is coming through
# mark cart complete
# mark order done

class QuotationSerializer(serializers.ModelSerializer):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	class Meta:
		model = Quotation
		fields= '__all__'
		# fields = []


class FinalizedOrderSerializer(TokenMixin, serializers.Serializer):
	order_token = serializers.CharField()
	payment_method_nonce = serializers.CharField()
	order_id =  serializers.IntegerField(required=False)
	user_checkout_id = serializers.IntegerField(required=False)


	def validate(self, data):
		order_token = data.get("order_token")
		order_data = self.parse_token(order_token)
		order_id = order_data.get("order_id")
		user_checkout_id = order_data.get("user_checkout_id")

		try:
			order_obj = Order.objects.get(id=order_id, user__id=user_checkout_id)
			data["order_id"] = order_id
			data["user_checkout_id"] = user_checkout_id
		except:
			raise serializers.ValidationError("This is not a valid order for this user.")

		payment_method_nonce = data.get("payment_method_nonce")
		if payment_method_nonce == None:
			raise serializers.ValidationError("This is not a valid payment method nonce")

		return data
	


class OrderDetailSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="order_detail_api")
	subtotal = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = [
			"url",
			"order_id",
			"user",
			"shipping_address",
			"billing_address",
			"shipping_total_price",
			"subtotal",
			"order_total",
		]

	def get_subtotal(self, obj):
		return obj.cart.subtotal



class OrderSerializer(serializers.ModelSerializer):
	subtotal = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = [
			"id",
			"user",
			"shipping_address",
			"billing_address",
			"shipping_total_price",
			"subtotal",
			"order_total",
		]

	def get_subtotal(self, obj):
		return obj.cart.subtotal



class UserAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserAddress
		fields = [
			"id",
			"user",
			"type",
			"street",
			"state",
			"city",
			"zipcode",
			"phone"
		]

	def create(self,  validated_data):
		user = self.context['request'].user
		usercheckout = UserCheckout.objects.filter(user_id=user.id).first()
		
		if usercheckout is None:

			usercheckout = UserCheckout()
			usercheckout.user_id = user.id
			usercheckout.email = user.email
			usercheckout.braintree_id = '0'
			usercheckout.save()

		useraddress = UserAddress.objects.filter(user_id=usercheckout.id).first()
		if useraddress is None:
			print('sadsd')
			useraddress = UserAddress()

		useraddress.user_id = usercheckout.id
		useraddress.type = validated_data.get('type')
		useraddress.street = validated_data.get('street')
		useraddress.city =  validated_data.get('city')
		useraddress.zipcode = validated_data.get('zipcode')
		useraddress.state = validated_data.get('state')
		useraddress.phone = validated_data.get('phone')
		useraddress.save()
		return useraddress


from . import service as OrderService
class CartOrderSerializer(serializers.ModelSerializer):
	order_total = serializers.DecimalField(required=False, max_digits=50, decimal_places=2,)
	class Meta:
		model = Order
		fields = '__all__'

	def create(self, validated_data):
		#pprint.pprint(self.context['request'].__dict__)
		#pprint.pprint(validated_data)
		user =  self.context['request'].user
		print( type(validated_data))
		#pprint.pprint(validated_data)
		validated_data['user_id'] = user.id

		order = OrderService.CreateOrderFromCart(validated_data)
		return order

	def saveStoreWiseOrder(self, order, user):
		print('order::')
		print(order)
		cart = order.cart
		cart_items = cart.items
		cart_items = CartItem.objects.filter(cart_id=cart.id)
		ordered_by = Store.objects.filter(fk_user_id=user.id).first()
		#ordered_by_store = ordered_by.id
		#print(ordered_by_store)

		# print('asdasdasdasd')
		for variation in cart_items:
			print(variation)
			store = variation.item.product.fk_store
			order_id = order.order_id
			store_id = store.id
			store_wise = StoreWiseOrder.objects.filter(order_id=order_id).filter(fk_ordered_store_id=store_id).first()
			if store_wise is None:			
				store_wise = StoreWiseOrder()
			store_wise.order_id = order.order_id
			store_wise.order_total = order.order_total
			store_wise.billing_address = order.billing_address
			store_wise.shipping_address = order.shipping_address
			store_wise.user_id = order.user_id
			store_wise.cart_id = order.cart_id
			store_wise.fk_auth_user_id = order.fk_auth_user_id
			store_wise.order_latitude = order.order_latitude
			store_wise.order_longitude = order.order_longitude
			store_wise.fk_ordered_store = store
			store_wise.fk_ordered_by_store = ordered_by
			store_wise.fk_payment_method = order.fk_payment_method
			store_wise.save()
			variation.fk_storewise_order_id = store_wise.id
			variation.save()
		store_wise_orders = StoreWiseOrder.objects.filter(order_id=order_id) 
		for store_wise_order in store_wise_orders:
			sw_cart_items =  CartItem.objects.filter(fk_storewise_order_id=store_wise_order.id) #store_wise_order.fk_storewise_order_id
			store_wise_order.order_total = 0
			# is_depo = Store.objects.filter(fk_user_id=user.id).filter(fk_store_type_id=2).first()
			# if not is_depo:
			if store_wise_order.order_latitude and store_wise_order.order_longitude:
				store_wise_order.fk_route = get_nearest_route(
					store_wise_order.order_latitude,
					store_wise_order.order_longitude,
					store_wise_order.fk_ordered_store.id,
					None
				)
			for cart_item in sw_cart_items:
				store_wise_order.order_total+=cart_item.line_item_total

			store_wise_order.save()


			# print(variation.product)




class OrderListStoreSerializer(serializers.ModelSerializer):
	billing_address = serializers.SerializerMethodField()
	mobile = serializers.SerializerMethodField()
	payment_method = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = ['id', 'status', 'is_delivered', 'is_paid', 
		'order_longitude', 'order_latitude', 'cart', 'user', 'order_total',
		'billing_address', 'fk_ordered_store', 'fk_delivery_user',
		 'fk_payment_method', 'mobile', "payment_method"]

	def get_billing_address(self, obj):
		return str(obj.billing_address.street)

	def get_mobile(self, obj):
		return obj.user.user.mobile

	def get_payment_method(self, obj):
		title=""
		if obj.fk_payment_method:
			title = obj.fk_payment_method.title		
		return title



class StoreWiseOrderListSerializer(serializers.ModelSerializer):
	# billing_address = serializers.SerializerMethodField()
	ordered_stored_name = serializers.SerializerMethodField()
	total_order_price = serializers.SerializerMethodField()
	customer_name = serializers.SerializerMethodField()
	address = serializers.SerializerMethodField()
	status = serializers.SerializerMethodField()
	created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

	class Meta:
		model = StoreWiseOrder
		fields = [

			"id",
            "shipping_total_price",
            "order_total",
            "order_id",
            "is_delivered",
            "is_paid",
            "is_transit",
            "created_at",
            "updated_at",
            "order_latitude",
            "order_longitude",
            "cart",
            "fk_auth_user",
            "fk_ordered_store",
            "fk_delivery_user",
            "fk_payment_method",
            "fk_ordered_by_store_id",
            "ordered_stored_name",
            "total_order_price",
            "customer_name",
            "address",
            "status"
            

		]

	def get_status(self, obj):
		status = "pending"
		if obj.is_delivered:
			status = "delivered"
		elif obj.is_transit:
			status = "transit"

		return status

	def get_ordered_stored_name(self, obj):
		abc = ""
		abc = Store.objects.filter(pk=obj.fk_ordered_by_store_id).first()
	
		if abc:
			return abc.title

		return abc
	def get_address(self, obj):
		cutomer_address = ""
		customer_address = UserAddress.objects.filter(user_id=obj.fk_auth_user_id).first()
		if customer_address:
			return str(customer_address.city + customer_address.street)
		return cutomer_address

	def get_customer_name(self, obj):

		customer_name = ""
		customer_name = User.objects.filter(pk=obj.fk_auth_user_id).first()
		print(customer_name)
		if customer_name:
			return customer_name.username
		return customer_name

	def get_total_order_price(self, obj):
		total_price = ""
		total_price = Order.objects.filter(order_id=obj.order_id).first()
		if total_price:
			total_price = total_price.order_total
		return total_price
		# def get_ordered_by(self, obj):
		# 	print(obj)
		# 	ordered_by = ""
		# 	if obj.fk_ordered_by_store_id:
		# 		ordered_by = Store.objects.filter(pk=obj.fk_ordered_by_store_id)
		# 	return ordered_by
	# def get_billing_address(self, obj):
	# 	return str(obj.billing_address.street)

	# def get_mobile(self, obj):
	# 	return obj.user.user.mobile


class UpdateOrderStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'



class UpdateStoreWiseOrderStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = StoreWiseOrder
		fields = '__all__'




class CartOrderListStoreSerializer(serializers.ModelSerializer):
	# cart_orders = serializers.SerializerMethodField()
	class Meta:
		model = CartItem
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
		]

	def get_item(self,obj):
		return obj.item.id

	def get_product_id(self, obj):
		return obj.id
		
	def get_item_title(self, obj):
		return "%s %s" %(obj.item.product.title, obj.item.title)

	def get_product(self, obj):
		return obj.item.product.id

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
		# print(obj.item.id)
		# print(obj.__dict__)
		# print(image_url)
		# return ""
		# print(list(image_url.values('image')))
		
		imageUrl = "/static/no-image.jpg"
		if image_url:
			d = image_url.__dict__
			if 'image' in d:
				imageUrl = d['image']



		# return image_url.image

		return imageUrl


		# cart_items = CartItem.objects.filter(cart_id=cart.id)





