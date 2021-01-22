import ast
import base64
import braintree

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin
from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
# from rest_framework.permissions import AllowAny
from rest_framework import permissions
from orders.forms import GuestCheckoutForm
from orders.mixins import CartOrderMixin
from orders.models import UserCheckout, Order, UserAddress
from orders.serializers import OrderSerializer, FinalizedOrderSerializer
from products.models import Variation, UserVariationQuantityHistory
from .mixins import TokenMixin, CartUpdateAPIMixin, CartTokenMixin
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CheckoutSerializer, AddToCartSerializer, CartItemModelSerializer, RemoveCartItemFromCartSerializer
from products.serializers import UserVariationQuantityHistorySerializer
from django.contrib.auth import get_user_model
from decimal import Decimal
User = get_user_model()

# 
# abc123

"""
{
	"order_token": "eydvcmRlcl9pZCc6IDU1LCAndXNlcl9jaGVja291dF9pZCc6IDExfQ==",
	"payment_method_nonce": "2bd23ca6-ae17-4bed-85f6-4d00aabcc3b0"

}


Run Python server:

python -m SimpleHTTPServer 8080

"""
class CheckoutFinalizeAPIView(TokenMixin, APIView):
	def get(self, request, format=None):
		response = {}
		order_token = request.GET.get('order_token')
		if order_token:
			checkout_id = self.parse_token(order_token).get("user_checkout_id")
			if checkout_id:
				checkout = UserCheckout.objects.get(id=checkout_id)
				client_token = checkout.get_client_token()
				response["client_token"] = client_token
				return Response(response)
		else:
			response["message"] = "This method is not allowed"
			return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


	def post(self, request, format=None):
		data = request.data
		response = {}
		serializer = FinalizedOrderSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			request_data = serializer.data
			order_id = request_data.get("order_id")
			order = Order.objects.get(id=order_id)
			if not order.is_complete:
				order_total = order.order_total
				nonce = request_data.get("payment_method_nonce")
				if nonce:
					result = braintree.Transaction.sale({
					    "amount": order_total,
					    "payment_method_nonce": nonce,
					    "billing": {
						    "postal_code": "%s" %(order.billing_address.zipcode),
						    
						 },
					    "options": {
					        "submit_for_settlement": True
					    }
					})
					success = result.is_success
					if success:
						#result.transaction.id to order
						order.mark_completed(order_id=result.transaction.id)
						#order.mark_completed(order_id="abc12344423")
						order.cart.is_complete()
						response["message"] = "Your order has been completed."
						response["final_order_id"] = order.order_id
						response["success"] = True
					else:
						#messages.success(request, "There was a problem with your order.")
						error_message = result.message
						#error_message = "Error"
						response["message"] = error_message
						response["success"] = False
			else:
				response["message"] = "Ordered has already been completed."
				response["success"] = False

		return Response(response)



class CheckoutAPIView(TokenMixin, APIView):

	def post(self, request, format=None):
		data = request.data
		serializer = CheckoutSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			#print "valid data!!@!@"
			data = serializer.data
			user_checkout_id = data.get("user_checkout_id")
			cart_id = data.get("cart_id")
			billing_address = data.get("billing_address")
			shipping_address = data.get("shipping_address")

			user_checkout = UserCheckout.objects.get(id=user_checkout_id)
			cart_obj = Cart.objects.get(id=cart_id)
			s_a = UserAddress.objects.get(id=shipping_address)
			b_a = UserAddress.objects.get(id=billing_address)
			order, created = Order.objects.get_or_create(cart=cart_obj, user=user_checkout)
			if not order.is_complete:
				order.shipping_address = s_a
				order.billing_address = b_a
				order.save()
				order_data = {
					"order_id": order.id,
					"user_checkout_id": user_checkout_id
				}
				order_token = self.create_token(order_data)
		response = {
			"order_token": order_token
		}
		return Response(response)


	# def get(self, request, format=None):
	# 	data, cart_obj, response_status = self.get_cart_from_token()

	# 	user_checkout_token = self.request.GET.get("checkout_token")
	# 	user_checkout_data = self.parse_token(user_checkout_token)
	# 	user_checkout_id = user_checkout_data.get("user_checkout_id")
	# 	billing_address = self.request.GET.get("billing")
	# 	shipping_address = self.request.GET.get("shipping")
	# 	billing_obj, shipping_obj = None, None
		
	# 	try:
	# 		user_checkout = UserCheckout.objects.get(id = int(user_checkout_id))
	# 	except:
	# 		user_checkout = None

	# 	if user_checkout == None:
	# 		data = {
	# 			"message": "A user or guest user is required to continue."
	# 		}
	# 		response_status = status.HTTP_400_BAD_REQUEST
	# 		return Response(data, status=response_status)

	# 	if billing_address:
	# 		try:
	# 			billing_obj = UserAddress.objects.get(user=user_checkout, id=int(billing_address))
	# 		except:
	# 			pass
		
	# 	if shipping_address:
	# 		try:
	# 			shipping_obj = UserAddress.objects.get(user=user_checkout, id=int(shipping_address))
	# 		except:
	# 			pass

	# 	if not billing_obj or not shipping_obj:
	# 		data = {
	# 			"message": "A valid billing or shipping is needed."
	# 		}
	# 		response_status = status.HTTP_400_BAD_REQUEST
	# 		return Response(data, status=response_status)


	# 	if cart_obj:
	# 		if cart_obj.items.count() == 0:
	# 			data = {
	# 				"message": "Your cart is Empty."
	# 			}
	# 			response_status = status.HTTP_400_BAD_REQUEST
	# 		else:
	# 			order, created = Order.objects.get_or_create(cart=cart_obj)
	# 			if not order.user:
	# 				order.user = user_checkout
	# 			if order.is_complete:
	# 				order.cart.is_complete()
	# 				data = {
	# 					"message": "This order has been completed."
	# 				}
	# 				return Response(data)
	# 			order.billing_address = billing_obj
	# 			order.shipping_address = shipping_obj
	# 			order.save()
	# 			data = OrderSerializer(order).data
	# 	return Response(data, status=response_status)




class CartAPIView(CartTokenMixin, CartUpdateAPIMixin, APIView):
	#authentication_classes = [SessionAuthentication]
	#permission_classes = [IsAuthenticated]
	token_param = "token"
	cart = None
	def get_cart(self):
		data, cart_obj, response_status = self.get_cart_from_token()
		# if cart_obj == None or not cart_obj.active:
		print(cart_obj)
		if cart_obj == None:

			cart = Cart()
			cart.tax_percentage = settings.TAX_PERCENT_DECIMAL#0.13
			if self.request.user.is_authenticated:
				cart.user = self.request.user
			cart.save()
			data = {
				"cart_id": str(cart.id)
			}
			self.create_token(data)
			cart_obj = cart

		return cart_obj


	def get(self, request, format=None):
		cart = self.get_cart()
		self.cart = cart
		self.update_cart()
		#token = self.create_token(cart.id)
		items = CartItemSerializer(cart.cartitem_set.all(), many=True)
		print(items)
		print(cart.items.all())
		data = {
			"token": self.token,
			"cart" : cart.id,
			"total": cart.total,
			"subtotal": cart.subtotal,
			"tax_total": cart.tax_total,
			"count": cart.items.count(),
			"items": items.data,
			# "product_id": items.id,
		}
		# print(cart.items)
		return Response(data)


# class PastCartAPIView(CartTokenMixin, CartUpdateAPIMixin, APIView):
# 	# authentication_classes = [SessionAuthentication]
# 	# permission_classes = [IsAuthenticated]
# 	token_param = "token"
# 	cart = None
# 	def get_cart(self):
# 		# data, cart_obj, response_status = self.get_cart_from_token()
# 		# if cart_obj == None or not cart_obj.active:

# 		print(cart_obj)
# 		if cart_obj == None:

# 			cart = Cart()
# 			cart.tax_percentage = settings.TAX_PERCENT_DECIMAL #0.13
# 			if self.request.user.is_authenticated:
# 				cart.user = self.request.user
# 			cart.save()
# 			data = {
# 				"cart_id": str(cart.id)
# 			}
# 			self.create_token(data)
# 			cart_obj = cart

# 		return cart_obj


# 	def get(self, request, format=None):
# 		cart = self.get_cart()
# 		self.cart = cart
# 		self.update_cart()
# 		#token = self.create_token(cart.id)
# 		items = CartItemSerializer(cart.cartitem_set.all(), many=True)
# 		print(items)
# 		print(cart.items.all())
# 		data = {
# 			"token": self.token,
# 			"cart" : cart.id,
# 			"total": cart.total,
# 			"subtotal": cart.subtotal,
# 			"tax_total": cart.tax_total,
# 			"count": cart.items.count(),
# 			"items": items.data,
# 			# "product_id": items.id,
# 		}
# 		# print(cart.items)
# 		return Response(data)


if settings.DEBUG:
	braintree.Configuration.configure(braintree.Environment.Sandbox,
      merchant_id=settings.BRAINTREE_MERCHANT_ID,
      public_key=settings.BRAINTREE_PUBLIC,
      private_key=settings.BRAINTREE_PRIVATE)


# from .models import UserMembershipAutoOrder
from carts.service import CartItemCreateService
from orders.service import CreateOrderFromCart, VariationHistoryCountService

from carts.models import Cart


from account.serializer import CreateUserSerializer
import random, string
def randomword(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))
class AddToCartForCustomUserAPIView(APIView):
	serializer_class = CartItemSerializer
	def post(self, request, *args, **kwargs):
		print(request.data)
		item_id = request.data.get('item_id')
		phone = request.data.get('phone')
		firstname = request.data.get('firstname', ' ')
		lastname = request.data.get('lastname', ' ')
		nickname = request.data.get('nick_name', ' ')
		user = User.objects.filter(mobile__iexact=phone).first()
		if not phone:
			return Response('Phone number is required.', status=400)
		print('user', user)
		if not user:
			# return Response({"Fail": phone+ " is not registered, please register"}, status.HTTP_400_BAD_REQUEST)
			temp_data = {
						'mobile': phone,
						'password': randomword(8),
						'email': randomword(8)+'@gmail.com',
						'nick_name': nickname,
						'username': phone,
						'firstname': firstname,
						'lastname':lastname

					}
			serializer = CreateUserSerializer(data = temp_data)
			serializer.is_valid(raise_exception = True)
			user = serializer.save()
			# old.delete()
			print('new user section')
		quantity = Decimal(request.data.get('quantity',0))
		cash = request.data.get('cash', 0) #debit ho
		ordered_price = request.data.get('ordered_price', 0)
		# user_id = user.id
		credit = request.data.get('credit')
		comment = request.data.get('comment')
		debit=cash
		# user_id = um_auto_order.fk_usermembership.fk_member_user_id
		data = {
			'user_id': user.id,
			'item_id': item_id,
			'quantity': quantity,
			'ordered_price': ordered_price,
			'is_auto_order': True,
			'credit': credit,
			'debit': debit,
			'fk_delivery_user_id' : request.user.id
		}
		print(data)
		CartItemCreateService(data)
		auto_carts = Cart.objects.filter(active=1).filter(is_auto_order=True).filter(user=user).all()
		# import pprint
		# pprint.pprint(auto_carts)
		for cart in auto_carts:
			order_data = {
			'user_id': user.id,
			'order_latitude': 1,
			'order_longitude': 1,
			'is_auto_order': True,
			'fk_payment_method': 1,
			'is_delivered': 1,
			'fk_delivery_user_id' : request.user.id
			}
			print( order_data )
			CreateOrderFromCart( order_data ) #
			vh_data = {
				"cart_id":cart.id,
				"comment": comment,
				"sign" : 1
			}
			VariationHistoryCountService(vh_data)
			pass
		return Response({'Success': 'Saved sucessfully'}, status=200)
		# cart = Cart.objects.filter(user_id=user_id).filter(active=1).first()
		# if not cart: 
		# 	cart = Cart()
		# 	cart.user_id = user_id
		# 	cart.save()
		# 	# print(cart)
		# cartitem = CartItem()
		# cartitem.item_id = item_id
		# cartitem.quantity = quantity
		# cartitem.ordered_price = cash
		# cartitem.cart = cart
		# cartitem.save()
		# serializer = CartItemModelSerializer(cartitem)
		# return Response(serializer.data)


from carts.models import Comment
class ReturnToStoreForCustomUserAPIView(APIView):
	# serializer_class = CartItemSerializer
	def post(self, request, *args, **kwargs):
		print(request.data)
		item_id = request.data.get('item_id')
		phone = request.data.get('phone')
		comment = request.data.get('comment')
		user = User.objects.filter(mobile__iexact=phone).first()
		if not user:
			return Response({"Fail": phone+ " is not registered, please register"}, status.HTTP_400_BAD_REQUEST)
		quantity = int(request.data.get('quantity'))
		# cash = request.data.get('cash', 0) #debit ho
		# ordered_price = request.data.get('ordered_price')
		# user_id = user.id
		# credit = request.data.get('credit')
		# debit=cash
		# user_id = um_auto_order.fk_usermembership.fk_member_user_id
		data = {
			'user_id': user.id,
			'item_id': item_id,
			'quantity': quantity, #this is returned quantity of the user
			'comment' : comment
			# 'ordered_price': ordered_price,
			# 'is_auto_order': True,
			# 'credit': credit,
			# 'debit': debit
		}
		print(data)
		query = UserVariationQuantityHistory.objects.filter(user_id=user.id).filter(variation_id=item_id)
		
		qs = query.first()
		if qs:
			if qs.num_delta==0:
				data = {}
				seriailzer = UserVariationQuantityHistorySerializer(qs, read_only=True)
				message = {'Fail': 'There is no pending Jars in this Account'}
				data = {
					"error" : message,
					"items": seriailzer.data
				}
				return Response(data, status=400) 
			qs.num_delta = qs.num_delta-quantity
			qs.save()
			# if comment:
			# 	if qs.comment is None:
			# 		qs.comment = ''
			# 	qs.comment += ', '+comment
			# if qs.num_delta < 1.0 :
			# 	qs.comment = ''
			if comment:
				cmnt = Comment()
				cmnt.comment = comment
				cmnt.user = user
				cmnt.save()
			
			seriailzer = UserVariationQuantityHistorySerializer(qs, read_only=True)
			return Response(seriailzer.data)
		else:
			return Response({'Fail': 'The Jar seems to be different than delivered'}, status=400) 
		
		

		# CartItemCreateService(data)
		# auto_carts = Cart.objects.filter(active=1).filter(is_auto_order=True).filter(user=user).all()
		# # import pprint
		# # pprint.pprint(auto_carts)
		# for cart in auto_carts:
		# 	order_data = {
		# 	'user_id': user.id,
		# 	'order_latitude': 1,
		# 	'order_longitude': 1,
		# 	'is_auto_order': True,
		# 	'fk_payment_method': 1
		# 	}
		# 	print( order_data )
		# 	CreateOrderFromCart( order_data )
		# 	VariationHistoryCountService(cart.id)
		# 	pass
		return Response({'Success': 'Updated Sucessfully'},status=200)



class ItemCountView(View):
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			# cart_id = self.request.session.get("cart_id")
			cart = Cart.objects.filter(user_id=request.user.id).first()

			cart_id = cart.id
			if cart_id == None:
				count = 0
			else:
				cart = Cart.objects.get(id=cart_id)
				count = cart.items.count()
			request.session["cart_item_count"] = count
			return JsonResponse({"count": count})
		else:
			raise Http404


class AddToCartView(CreateAPIView):
	# permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset=CartItem.objects.all()
	serializer_class = CartItemModelSerializer 
	# serializer_class = RemoveCartItemFromCartSerializer 





class RemoveCartItemFromCart(DestroyAPIView):
	# permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset=CartItem.objects.all()
	serializer_class = RemoveCartItemFromCartSerializer




class CartView(SingleObjectMixin, View):
	model = Cart
	template_name = "carts/view.html"

	def get_object(self, request, *args, **kwargs):
		# self.request.session.set_expiry(0) #5 minutes
		# cart_id = self.request.session.get("cart_id")
		# if(request.is_ajax()):
		# 	print("true")

		
		cart = Cart.objects.filter(user_id=self.request.user.id).first()
		print('-----------------------')
		print(cart)
	

		# cart_id = cart.id
		# if cart_id == None:
		if cart == None:
			cart = Cart()
			cart.tax_percentage =  settings.TAX_PERCENT_DECIMAL #0.13
			cart.save()
			# cart_id = cart.id

			# self.request.session["cart_id"] = cart_id
			# Cart.objects.filter(user_id=self.request.user.id).first().id= cart_id
		cart_id = cart.id
		# cart = Cart.objects.get(id=cart_id)
		if self.request.user.is_authenticated:
			cart.user = self.request.user
			cart.save()
		return cart

	def get(self, request, *args, **kwargs):
		cart = self.get_object(request.user.id)
		# cart = Cart.objects.filter(user_id=request.user.id).first()
		print('-----------')
		print(cart)
		# item_id = cart_id
		item_id = request.GET.get("item")
		delete_item = request.GET.get("delete", False)
		flash_message = ""
		item_added = False
		if item_id:
			item_instance = get_object_or_404(Variation, id=item_id)
			qty = request.GET.get("qty", 1)
			try:
				if int(qty) < 1:
					delete_item = True
			except:
				raise Http404
			cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
			if created:
				flash_message = "Successfully added to the cart"
				item_added = True
			if delete_item:
				flash_message = "Item removed successfully."
				cart_item.delete()
			else:
				if not created:
					flash_message = "Quantity has been updated successfully."
				cart_item.quantity = qty
				cart_item.save()
			if not request.is_ajax():
				return HttpResponseRedirect(reverse("cart"))
				#return cart_item.cart.get_absolute_url()
		
		if request.is_ajax():
			try:
				total = cart_item.line_item_total
			except:
				total = None
			try:
				subtotal = cart_item.cart.subtotal
			except:
				subtotal = None

			try:
				cart_total = cart_item.cart.total
			except:
				cart_total = None

			try:
				tax_total = cart_item.cart.tax_total
			except:
				tax_total = None

			try:
				total_items = cart_item.cart.items.count()
			except:
				total_items = 0

			data = {
					"deleted": delete_item, 
					"item_added": item_added,
					"line_total": total,
					"subtotal": subtotal,
					"cart_total": cart_total,
					"tax_total": tax_total,
					"flash_message": flash_message,
					"total_items": total_items
					}

			return JsonResponse(data) 


		context = {
			"object": self.get_object(request)
		}
		template = self.template_name
		return render(request, template, context)




class CheckoutView(CartOrderMixin, FormMixin, DetailView):
	model = Cart
	template_name = "carts/checkout_view.html"
	form_class = GuestCheckoutForm

	def get_object(self, *args, **kwargs):
		cart = self.get_cart()
		if cart == None:
			return None
		return cart

	def get_context_data(self, *args, **kwargs):
		context = super(CheckoutView, self).get_context_data(*args, **kwargs)
		user_can_continue = False
		user_check_id = self.request.session.get("user_checkout_id")
		if self.request.user.is_authenticated:
			user_can_continue = True
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user = self.request.user
			user_checkout.save()
			context["client_token"] = user_checkout.get_client_token()
			self.request.session["user_checkout_id"] = user_checkout.id
		elif not self.request.user.is_authenticated and user_check_id == None:
			context["login_form"] = AuthenticationForm()
			context["next_url"] = self.request.build_absolute_uri()
		else:
			pass

		if user_check_id != None:
			user_can_continue = True
			if not self.request.user.is_authenticated(): #GUEST USER
				user_checkout_2 = UserCheckout.objects.get(id=user_check_id)
				context["client_token"] = user_checkout_2.get_client_token()
		
		#if self.get_cart() is not None:
		context["order"] = self.get_order()
		context["user_can_continue"] = user_can_continue
		context["form"] = self.get_form()
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			email = form.cleaned_data.get("email")
			user_checkout, created = UserCheckout.objects.get_or_create(email=email)
			request.session["user_checkout_id"] = user_checkout.id
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse("checkout")


	def get(self, request, *args, **kwargs):
		get_data = super(CheckoutView, self).get(request, *args, **kwargs)
		cart = self.get_object()
		if cart == None:
			return redirect("cart")
		new_order = self.get_order()
		user_checkout_id = request.session.get("user_checkout_id")
		if user_checkout_id != None:
			user_checkout = UserCheckout.objects.get(id=user_checkout_id)
			if new_order.billing_address == None or new_order.shipping_address == None:
			 	return redirect("order_address")
			new_order.user = user_checkout
			new_order.save()
		return get_data






class CheckoutFinalView(CartOrderMixin, View):
	def post(self, request, *args, **kwargs):
		order = self.get_order()
		order_total = order.order_total
		nonce = request.POST.get("payment_method_nonce")
		if nonce:
			result = braintree.Transaction.sale({
			    "amount": order_total,
			    "payment_method_nonce": nonce,
			    "billing": {
				    "postal_code": "%s" %(order.billing_address.zipcode),
				    
				 },
			    "options": {
			        "submit_for_settlement": True
			    }
			})
			if result.is_success:
				#result.transaction.id to order
				order.mark_completed(order_id=result.transaction.id)
				messages.success(request, "Thank you for your order.")
				del request.session["cart_id"]
				del request.session["order_id"]
			else:
				#messages.success(request, "There was a problem with your order.")
				messages.success(request, "%s" %(result.message))
				return redirect("checkout")

		return redirect("order_detail", pk=order.pk)

	def get(self, request, *args, **kwargs):
		return redirect("checkout")


















