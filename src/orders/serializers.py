from rest_framework import serializers

from carts.mixins import TokenMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import UserAddress, Order, Quotation, UserCheckout
from carts.models import Cart

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





class CartOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

	def create(self, validated_data):
		user =  self.context['request'].user
		
		# item_quantity = validated_data.pop('item_quantity')
		cart = Cart.objects.filter(user_id=user.id).filter(active=1).first()
		usercheckout_user = UserCheckout.objects.filter(user_id=user).first()
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
		order.shipping_total_price = 100
		order.order_total = cart.total
		order.billing_address = useraddress
		order.shipping_address = useraddress
		order.user_id = usercheckout_user.id
		order.cart_id = cart.id
		print(order.__dict__)
		order.save()


		cart.active=0
		cart.save()

		return order





		# cart_items = CartItem.objects.filter(cart_id=cart.id)





