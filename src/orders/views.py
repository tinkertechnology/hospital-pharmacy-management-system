from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
# Create your views here.

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from carts.mixins import TokenMixin
from rest_framework import permissions
from .forms import AddressForm, UserAddressForm, UserOrderForm
from .mixins import CartOrderMixin, LoginRequiredMixin
from .models import UserAddress, UserCheckout, Order, Quotation
from .permissions import IsOwnerAndAuth
from .serializers import UserAddressSerializer, OrderSerializer, OrderDetailSerializer, QuotationSerializer, CartOrderSerializer, \
		OrderListStoreSerializer, CartOrderListStoreSerializer, CartItemSerializer, UpdateOrderStatusSerializer, \
		StoreWiseOrderListSerializer, UpdateStoreWiseOrderStatusSerializer
import requests
from carts.models import Cart, CartItem
from store.models import Store, StoreUser
from orders.models import StoreWiseOrder
from products.models import Product, Variation
from django.conf import settings
from django.db.models import Q
User = get_user_model()


""" 

Notes for changes.


"""

def AccountsVerifyRegistrationView(request):
	# return HttpResponse("return this string")
	# user_id = request.GET.get('user_id', '')
	# timestamp = request.GET.get('timestamp', '')
	# signature = request.GET.get('signature', '')
	url = 'http://'+ request.get_host() + '/accounts/verify-registration/'
	requests.post( url,data=request.GET)
	return HttpResponse("success Account Verified")

def AccountsResetPasswordView(request):
	# url = 'http://'+ request.get_host() + '/accounts/reset-password/'
	# requests.post( url,data=request.GET)
	return render(request, 'registration/password_reset_form.html', {'form':request.GET})


class SendQuotationApiView(CreateAPIView):
	model = Quotation
	serializer_class = QuotationSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	



class OrderRetrieveAPIView(RetrieveAPIView):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsOwnerAndAuth]
	model = Order
	queryset = Order.objects.all()
	serializer_class = OrderDetailSerializer

	def get_queryset(self, *args, **kwargs):
		return Order.objects.filter(user__user=self.request.user)


class OrderListAPIView(ListAPIView):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsOwnerAndAuth]
	model = Order
	queryset = Order.objects.all()
	serializer_class = OrderDetailSerializer

	def get_queryset(self, *args, **kwargs):
		return Order.objects.filter(user__user=self.request.user)




class UserAddressCreateAPIView(CreateAPIView):
	model = UserAddress
	serializer_class = UserAddressSerializer


class UserAddressListAPIView(TokenMixin, ListAPIView):
	model = UserAddress
	queryset = UserAddress.objects.all()
	serializer_class = UserAddressSerializer

	def get_queryset(self, *args, **kwargs):
		user_checkout_token = self.request.GET.get("checkout_token")
		user_checkout_data = self.parse_token(user_checkout_token)
		user_checkout_id = user_checkout_data.get("user_checkout_id")
		if self.request.user.is_authenticated:
			return UserAddress.objects.filter(user__user=self.request.user)
		elif user_checkout_id:
			return UserAddress.objects.filter(user__id=int(user_checkout_id))
		else:
			return []



class UserCheckoutMixin(TokenMixin, object):
	def user_failure(self, message=None):
		data = {
			"message": "There was an error. Please try again.",
			"success": False
		}
		if message:
			data["message"] = message
		return data


	def get_checkout_data(self, user=None, email=None):
		if email and not user:
			user_exists = User.objects.filter(email=email).count()
			if user_exists != 0:
				return self.user_failure(message="This user already exists, please login.")

		data = {}
		user_checkout = None
		if user and not email:
			if user.is_authenticated:
				user_checkout = UserCheckout.objects.get_or_create(user=user, email=user.email)[0] #(instance, created)
			
		elif email:
			try:
				user_checkout = UserCheckout.objects.get_or_create(email=email)[0]
				if user:
					user_checkout.user = user
					user_checkout.save()
			except:
				pass #(instance, created)
		else:
			pass

		if user_checkout:
			data["success"]= True
			data["braintree_id"] = user_checkout.get_braintree_id
			data["user_checkout_id"] = user_checkout.id
			data["user_checkout_token"] = self.create_token(data)
			
			del data["braintree_id"]
			del data["user_checkout_id"]
			data["braintree_client_token"] = user_checkout.get_client_token()

		return data


class UserCheckoutAPI(UserCheckoutMixin, APIView):
	permission_classes = [AllowAny]
	def get(self, request, format=None):
		data = self.get_checkout_data(user=request.user)
		return Response(data)

	def post(self, request, format=None):
		data = {}
		email = request.data.get("email")
		if request.user.is_authenticated:
			if email == request.user.email:
				data = self.get_checkout_data(user=request.user, email=email)
			else:
				data = self.get_checkout_data(user=request.user)
		elif email and not request.user.is_authenticated:
			data = self.get_checkout_data(email=email)
		else:
			data = self.user_failure(message="Make sure you are authenticated or using a valid email.")
		return Response(data)




class OrderDetail(DetailView):
	model = Order
	def dispatch(self, request, *args, **kwargs):
		try:
			user_check_id = self.request.session.get("user_checkout_id")
			user_checkout = UserCheckout.objects.get(id=user_check_id)
		except UserCheckout.DoesNotExist:
			user_checkout = UserCheckout.objects.get(user=request.user)
		except:
			user_checkout = None

		obj = self.get_object()
		if obj.user == user_checkout and user_checkout is not None:
			return super(OrderDetail, self).dispatch(request, *args, **kwargs)
		else:
			raise Http404




class OrderList(LoginRequiredMixin, ListView):
	queryset = Order.objects.all()

	def get_queryset(self):
		user_check_id = self.request.user.id
		user_checkout = UserCheckout.objects.get(id=user_check_id)
		return super(OrderList, self).get_queryset().filter(user=user_checkout)




class OrderLists(ListAPIView):
	# queryset = Order.objects.all()
	serializer_class = OrderListStoreSerializer

	def get_queryset(self):
		super_user = self.request.user.is_superuser
		filter_query = self.request.GET.get('status')
		if super_user:
			orders = orders = Order.objects.filter(status=1)
			if filter_query=="pending":
				print(1)
				orders = Order.objects.filter(status=1)
			if filter_query=="delivered":
				print(2)
				orders = Order.objects.filter(status=0)	
				print(orders.count())


		else:
			orders = Order.objects.filter(fk_auth_user_id=self.request.user.id).filter(status=1)
			if filter_query=="pending":
				orders = Order.objects.filter(fk_auth_user_id=self.request.user.id).filter(status=1)
			if filter_query=="delivered":
				orders = Order.objects.filter(fk_auth_user_id=self.request.user.id).filter(status=0)

		
		return orders



class StoreWiseOrderLists(ListAPIView):
	# queryset = Order.objects.all()
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = StoreWiseOrderListSerializer

	def get_queryset(self):
		filter = self.request.GET.get('filter')
		# from_date = self.request.GET.get('from_date')
		# to_date = self.request.GET.get('to_date')
		# from_date = '2020-07-18 00:00:00';
		# to_date = '2020-07-19 00:00:00';


		user=self.request.user
		# orders= Order.objects.filter(fk_auth_user_id=self.request.user.id)
		supply_store_user = Store.objects.filter(fk_user_id=self.request.user.id).first()
		delivery_user = StoreUser.objects.filter(fk_user_id=user.id).filter(fk_store_usertypes_id=2).first()
		
		if supply_store_user is not  None:
			print(supply_store_user.id)
			qs = StoreWiseOrder.objects.filter(fk_ordered_store_id=supply_store_user.id).filter(is_delivered=0)
			print(1) #.filter(is_delivered=0)
			if filter:
				if filter=='pending':
					qs = StoreWiseOrder.objects.filter(fk_ordered_store_id=supply_store_user.id).filter(is_delivered=0, is_transit=0)
				if filter=='transit':
					qs = StoreWiseOrder.objects.filter(fk_ordered_store_id=supply_store_user.id).filter(is_transit=1)
				if filter=='delivered':
					qs = StoreWiseOrder.objects.filter(fk_ordered_store_id=supply_store_user.id).filter(is_delivered=1)
		
		if delivery_user is not None:
			qs = StoreWiseOrder.objects.filter(fk_route_id=delivery_user.fk_route_id).filter(is_delivered=0)
			if filter:
				if filter=='pending':
					qs = StoreWiseOrder.objects.filter(fk_route_id=delivery_user.fk_route_id).filter(is_delivered=0, is_transit=0)
				if filter=='transit':
					qs = StoreWiseOrder.objects.filter(fk_route_id=delivery_user.fk_route_id).filter(is_transit=1)
				if filter=='delivered':
					qs = StoreWiseOrder.objects.filter(fk_route_id=delivery_user.fk_route_id).filter(is_delivered=1)

		if not supply_store_user:
			if not delivery_user:
				qs = StoreWiseOrder.objects.filter(fk_auth_user_id=self.request.user.id).filter(is_delivered=0)
				if filter:
					if filter=='pending':
						qs = StoreWiseOrder.objects.filter(fk_auth_user_id=self.request.user.id)
					if filter=='transit':
						qs = StoreWiseOrder.objects.filter(fk_auth_user_id=self.request.user.id).filter(is_transit=1)
					if filter=='delivered':
						qs = StoreWiseOrder.objects.filter(fk_auth_user_id=self.request.user.id).filter(is_delivered=1)
		# from datetime import datetime, timedelta, time
		# from django.utils.dateparse import parse_date
		# import dateutil.parser
		# if from_date:
		# 	print(12)
		# 	from_date = dateutil.parser.parse(from_date)
		# 	qs = qs.filter(created_at__gte=from_date) #(created_at__range=[from_date, to_date])
		# 	print(from_date)
		# if to_date:
		# 	print(21)
		# 	print(to_date)
		# 	to_date = dateutil.parser.parse(to_date)
		# 	qs = qs.filter(created_at__lt=to_date)
		print(qs.query)
		return qs

class OrderHistoryLists(ListAPIView):
	from django.db.models import Q
	# queryset = Order.objects.all()
	serializer_class = OrderListStoreSerializer

	def get_queryset(self):
		
		non_store_user = Store.objects.filter(fk_user_id=self.request.user.id).first()
		print(non_store_user)
		if non_store_user is None:
			# user_checkouts = UserCheckout.objects.filter(user_id=self.request.user.id).id
			# print(user_checkouts.__dict__)
			orders= Order.objects.filter(fk_auth_user_id=self.request.user.id).filter(Q(is_paid=True) | Q(is_delivered=True))
			
			
		else:
			orders = Order.objects.filter(status=1)			
			if settings.CAN_STORE_SEE_ALL_ORDERS==False:
				user_id = self.request.user.id
				store = Store.objects.filter(fk_user_id=user_id).first()
				if store is None:
					orders = []
				else:
					orders = orders.filter(fk_ordered_store=store).filter(Q(is_paid=True) | Q(is_delivered=True))
		
		return orders


class StoreWiseOrderHistoryLists(ListAPIView):
	from django.db.models import Q
	# queryset = Order.objects.all()
	serializer_class = StoreWiseOrderListSerializer

	def get_queryset(self):
		
		store_user = Store.objects.filter(fk_user_id=self.request.user.id).first()
	
		if store_user is None:
			# user_checkouts = UserCheckout.objects.filter(user_id=self.request.user.id).id
			# print(user_checkouts.__dict__)
			orders= StoreWiseOrder.objects.filter(fk_auth_user_id=self.request.user.id).filter(Q(is_paid=True) | Q(is_delivered=True))
			
			
		else:
			orders = StoreWiseOrder.objects.all()			
			if settings.CAN_STORE_SEE_ALL_ORDERS==False:
				user_id = self.request.user.id
				store = Store.objects.filter(fk_user_id=user_id).first()
				if store is None:
					orders = []
				else:
					orders = orders.filter(fk_ordered_store=store).filter(Q(is_paid=True) | Q(is_delivered=True))
		
		return orders



class CartOrderLists(ListAPIView):
	def get(self, request):

		order_id = request.query_params['order_id']
		order = Order.objects.get(id=order_id)
		cart = Cart.objects.get(id=order.cart_id)

		# self.cart = cart
		# self.update_cart()
		#token = self.create_token(cart.id)
		# items = CartItemSerializer(cart.cartitem_set.all(), many=True)
		items = CartItemSerializer(cart.cartitem_set.all(), many=True)
		print(items)
		print(cart.items.all())
		data = {
		# "token": self.token,
		"cart" : cart.id,
		"total": cart.total,
		"subtotal": cart.subtotal,
		"tax_total": cart.tax_total,
		"count": cart.items.count(),
		"items": items.data,
		# "product_id": items.id,
		}
		return Response(data)
		# print(cart.items)
		# return Response(len(data))

	# queryset = Order.objects.all()

		# user_id = self.request.user.id
		# cart_id = 22
		# cart_items = CartItem.objects.all()
		# orders = Order.objects.filter(status=1, fk_ordered_store=1)
		# print(orders.__dict__)
		# return orders




##Storewise_CART_ORDER_LIST 
class StoreWiseCartOrderLists(ListAPIView):
	def get(self, request):

		order_id = request.GET.get('order_id', False) #fk_storewise_order_id passed here
		cart_items = CartItem.objects.filter(fk_storewise_order_id=order_id)
		# cart = Cart.objects.filter(id=cart_items)
		orders_list = []
		# total_item = {len(cart_items)}
		items = CartItemSerializer(cart_items, many=True)
		# print(items)
		cart = Cart()
		# print(cart.items.all())
		data = {
		# "token": self.token,
		"cart" : cart.id,
		"total": cart.total,
		"subtotal": cart.subtotal,
		"tax_total": cart.tax_total,
		"count": cart_items.count(),
		"items": items.data,
		# "product_id": items.id,
		}
		return Response(data)

		# # print(total_item)
		# for item in cart_items:

		# 	data = {
		# 	"line_item_total": item.line_item_total,
		# 	"id": item.id,
		# 	"product_title": item.item.product.title,
		# 	"quantity": item.quantity,
		# 	"price": item.item.product.price,
		# 	"fk_storewise_order_id": item.fk_storewise_order_id

		# 	}
		# # 	print(a)
		# # 	b = a.update(a)
		# # 	print(b)

		# # return Response(b)
		# 	orders_list.append(data)
		# 	print(orders_list)

		# return Response(orders_list)

	def get_queryset(self):
		return 
# 		alist = []
# for x in range(100):
#     adict = {1:x}
#     alist.append(adict)
# print(alist)
		# print(cart)

		# self.cart = cart
		# self.update_cart()
		#token = self.create_token(cart.id)
		# items = CartItemSerializer(cart.cartitem_set.all(), many=True)
		# a = {}
		# for item in cart_items:
		# 	items = CartItemSerializer(item.cartitem_set.all(), many=True)
		# 	data = {
		# 	# "token": self.token,
		# 	"cart" : item.id,
		# 	"total": item.total,
		# 	"subtotal": item.subtotal,
		# 	"tax_total": item.tax_total,
		# 	"count": item.items.count(),
		# 	"items": items.data,
		# 	# "product_id": items.id,
		# 	}
		# 	a = a.update(data)
		# return Response(a)


		# print(cart.items)
		# return Response(len(data))

	# queryset = Order.objects.all()

		# user_id = self.request.user.id
		# cart_id = 22
		# cart_items = CartItem.objects.all()
		# orders = Order.objects.filter(status=1, fk_ordered_store=1)
		# print(orders.__dict__)
		# return orders

class UserAddressCreateView(CreateView):
	form_class = UserAddressForm
	template_name = "forms.html"
	success_url = "/checkout/address/"

	def get_checkout_user(self):
		user_check_id = self.request.session.get("user_checkout_id")
		user_checkout = UserCheckout.objects.get(id=user_check_id)
		return user_checkout

	def form_valid(self, form, *args, **kwargs):
		form.instance.user = self.get_checkout_user()
		return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)



class AddressSelectFormView(CartOrderMixin, FormView):
	form_class = AddressForm
	template_name = "orders/address_select.html"


	def dispatch(self, *args, **kwargs):
		b_address, s_address = self.get_addresses()
		if b_address.count() == 0:
			messages.success(self.request, "Please add a billing address before continuing")
			return redirect("user_address_create")
		elif s_address.count() == 0:
			messages.success(self.request, "Please add a shipping address before continuing")
			return redirect("user_address_create")
		else:
			return super(AddressSelectFormView, self).dispatch(*args, **kwargs)


	def get_addresses(self, *args, **kwargs):
		user_check_id = self.request.session.get("user_checkout_id")
		user_checkout = UserCheckout.objects.get(id=user_check_id)
		b_address = UserAddress.objects.filter(
				user=user_checkout,
				type='billing',
			)
		s_address = UserAddress.objects.filter(
				user=user_checkout,
				type='shipping',
			)
		return b_address, s_address


	def get_form(self, *args, **kwargs):
		form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
		b_address, s_address = self.get_addresses()

		form.fields["billing_address"].queryset = b_address
		form.fields["shipping_address"].queryset = s_address
		return form

	def form_valid(self, form, *args, **kwargs):
		billing_address = form.cleaned_data["billing_address"]
		shipping_address = form.cleaned_data["shipping_address"]
		order = self.get_order()
		order.billing_address = billing_address
		order.shipping_address = shipping_address
		order.save()
		return  super(AddressSelectFormView, self).form_valid(form, *args, **kwargs)

	def get_success_url(self, *args, **kwargs):
		return "/checkout/"



class CartOrderApiView(CreateAPIView):
	# permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset=Order.objects.all()
	serializer_class = CartOrderSerializer 


def UserOrderView(request):
	user_order_form = UserOrderForm()
	order_list = Order.objects.filter(status=1)
	# cart_items = Cart.cartitem_set.all()
	# print(cart_items)

	return render(request, 'orders/user_order.html', {'user_order':user_order_form, 'order_list':order_list})


def UserOrderDetailView(request, id):
	cart_items = CartItem.objects.filter(cart_id=id)
	order = Order.objects.get(cart_id=id)
	cart = Cart.objects.get(id=id)

	total_price = order.shipping_total_price + cart.total
	# cart_item_list = cart_items.item
	# print(cart_items.item)
	print(cart_items.__dict__)
	return render(request, 'orders/order_detail.html', {'cart_items':cart_items, 'order':order, 'cart':cart, 'total_price':total_price})

	# return HttpResponse('User Order Detail View')

class UpdateOrderStatusApiView(CreateAPIView): ## YO USE BHAKO CHAINA //STOREWISE ORDER HAINA
	# permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset=Order.objects.all()
	serializer_class = UpdateOrderStatusSerializer

	def post(self, request):
		import pprint
		pprint.pprint(request.POST)
		order_id = request.POST.get('order_id')
		status = request.POST.get('status')
		print(order_id)
		order = Order.objects.filter(pk=order_id).first() 
		if order:
			# if status == "paid":
			# 	order.is_paid = 1;
			# if status == "delivered":
			# 	order.is_delivered = 1;
			order.status=0
			order.save()

			return Response({
							'status': True,
							'detail': 'Order is marked as Delivered'
							})
		else:
			Response({"Fail": "Error updating order status"}, status.HTTP_400_BAD_REQUEST)



class UpdateStoreWiseOrderStatusApiView(CreateAPIView):
	# permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset=Order.objects.all()
	serializer_class = UpdateStoreWiseOrderStatusSerializer

	def post(self, request):
		import pprint
		pprint.pprint(request.POST)
		storewiseorder_id = request.POST.get('order_id') ### id of StoreWiseOrder model's.
		status = request.POST.get('status')
		storewiseorder = StoreWiseOrder.objects.filter(pk=storewiseorder_id).first()
		if storewiseorder:
			# for storewise_order in storewiseorder:
			if status == "paid":
				storewiseorder.is_paid = True;

			if status == "transit":
				storewiseorder.is_transit = True;

			if status == "delivered":
				storewiseorder.is_delivered = True;
				is_depo=storewiseorder.fk_ordered_by_store_id is not None
				if is_depo:
					self.addProductinStore(storewiseorder) #DEPO LE COMPANY SANGA KINDA DEPO MA BADXA
				else:
					self.subProductinStore(storewiseorder) ###CUSTOMER LE DEPO SANGA KINDA KHERI GHATCHA
			storewiseorder.save()

		#if settings.IS_MULTI_VENDOR:
			

			return Response({
							'status': True,
							'detail': 'Order is marked as '+status
							})
		else:
			Response({"Fail": "Error updating order status"}, status.HTTP_400_BAD_REQUEST)


	def addProductinStore(self,storewiseorder):
		buyer_store_id = storewiseorder.fk_ordered_by_store_id
		cartitems = CartItem.objects.filter(fk_storewise_order_id=storewiseorder.id)
		for cartitem in cartitems:
			seller_product = cartitem.item.product
			common_product = seller_product.fk_common_product
			buyer_product = Product.objects.filter(fk_store_id = buyer_store_id).filter(fk_common_product=common_product).first()

			if buyer_product is None:
				dict_buyer_product = seller_product.__dict__
				import pprint
				pprint.pprint(dict_buyer_product)
				dict_buyer_product.pop('id')
				dict_buyer_product.pop('_state')
				dict_buyer_product['fk_store_id'] = buyer_store_id
				buyer_product = Product.objects.create(**dict_buyer_product)
			buyer_variation = Variation.objects.filter(product_id=buyer_product.id).first()
			if buyer_variation.inventory is None:
				buyer_variation.inventory=0
			buyer_variation.inventory += cartitem.quantity
			buyer_variation.save()

	def subProductinStore(self, storewiseorder):
		cartitems = CartItem.objects.filter(fk_storewise_order_id=storewiseorder.id)
		for cartitem in cartitems:
			buyer_variation =  cartitem.item #Variation.objects.filter(product_id=buyer_product.id).first()
			if buyer_variation.inventory is None:
				buyer_variation.inventory=0
			buyer_variation.inventory -= cartitem.quantity
			buyer_variation.save()




class myStoreName(APIView):
	def get(self, request, *args, **kwargs):
		print(request.user.id)
		store_name=""
		get_store_name = Store.objects.filter(fk_user_id=request.user.id).first()
		if get_store_name:
			store_name = get_store_name.title
		return Response(store_name)


				
