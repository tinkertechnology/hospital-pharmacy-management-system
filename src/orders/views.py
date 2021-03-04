from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
# Create your views here.
from datetime import datetime, timedelta, time
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
import pytz

from carts.mixins import TokenMixin
from rest_framework import permissions
# from .forms import AddressForm, UserAddressForm, UserOrderForm
from .mixins import CartOrderMixin, LoginRequiredMixin
from .models import  Order#UserAddress, UserCheckout, Order, Quotation
from .permissions import IsOwnerAndAuth
from .serializers import  OrderSerializer, OrderDetailSerializer, CartOrderSerializer, \
		OrderListStoreSerializer, CartOrderListStoreSerializer, CartItemSerializer, UpdateOrderStatusSerializer, \
		StoreWiseOrderListSerializer, UpdateStoreWiseOrderStatusSerializer
import requests
from carts.models import Cart, CartItem
from store.models import Store, StoreUser
from orders.models import StoreWiseOrder
from products.models import Product, Variation, UserVariationQuantityHistory
from django.conf import settings
from django.db.models import Q
from products.models import Variation
from carts.models import TransactionType
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
	# permission_classes = [IsOwnerAndAuth]
	model = Order
	queryset = Order.objects.all()
	serializer_class = OrderDetailSerializer

	def get_queryset(self, *args, **kwargs):
		return Order.objects.filter(user__user=self.request.user)












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
				settings.DPRINT(1)
				orders = Order.objects.filter(status=1)
			if filter_query=="delivered":
				settings.DPRINT(2)
				orders = Order.objects.filter(status=0)	
				settings.DPRINT(orders.count())


		else:
			orders = Order.objects.filter(fk_auth_user_id=self.request.user.id).filter(status=1)
			if filter_query=="pending":
				orders = Order.objects.filter(fk_auth_user_id=self.request.user.id).filter(status=1)
			if filter_query=="delivered":
				orders = Order.objects.filter(fk_auth_user_id=self.request.user.id).filter(status=0)

		
		return orders


# from store.service import getUserStoreService
class StoreWiseOrderLists(ListAPIView):
	# queryset = Order.objects.all()
	
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = StoreWiseOrderListSerializer

	def get_queryset(self):
		settings.DLFPRINT()
		filter = self.request.GET.get('filter')
		# from_date = self.request.GET.get('from_date')
		# to_date = self.request.GET.get('to_date')
		# from_date = '2020-07-18 00:00:00';
		# to_date = '2020-07-19 00:00:00';
		user=self.request.user
		# orders= Order.objects.filter(fk_auth_user_id=self.request.user.id)
		supply_store_user = Store.objects.filter(fk_user_id=self.request.user.id).first()
		delivery_user = StoreUser.objects.filter(fk_user_id=user.id).filter(fk_store_usertypes_id=2).first()
		store = getUserStoreService(self.request.user.id)

		orderq =StoreWiseOrder.objects 
		if store is not  None: #depotmanager ko lagi
			# qs = StoreWiseOrder.objects.filter(fk_ordered_store_id=store.id).filter(is_delivered=0)
			settings.DPRINT(1) #.filter(is_delivered=0)
			orderq = orderq.filter(fk_ordered_store_id=store.id) #.filter(is_delivered=0)
		if filter:
			if filter=='pending':
				orderq = orderq.filter(is_delivered=0, is_transit=0, is_cancelled=0)
			elif filter=='transit':
				orderq = orderq.filter(is_transit=1)
			elif filter=='delivered':
				orderq = orderq.filter(is_delivered=1)
			elif filter=='cancelled':
				orderq = orderq.filter(is_cancelled=1)
		else:
			orderq = orderq.filter(is_delivered=0)
		if delivery_user is not None and False: #delivery-boy lai route anusar gareko
			orderq = orderq.filter(fk_route_id=delivery_user.fk_route_id).filter(is_delivered=0)
		if not supply_store_user: ##Yo normal-user-lai
			if not delivery_user:
				orderq = orderq.filter(fk_auth_user_id=self.request.user.id)		
		# from django.utils.dateparse import parse_date
		# import dateutil.parser
		# if from_date:
		# 	settings.DPRINT(12)
		# 	from_date = dateutil.parser.parse(from_date)
		# 	qs = qs.filter(created_at__gte=from_date) #(created_at__range=[from_date, to_date])
		# 	settings.DPRINT(from_date)
		# if to_date:
		# 	settings.DPRINT(21)
		# 	settings.DPRINT(to_date)
		# 	to_date = dateutil.parser.parse(to_date)
		# 	qs = qs.filter(created_at__lt=to_date)
		settings.DPRINT(orderq.query)
		return orderq#qs

class OrderHistoryLists(ListAPIView):
	from django.db.models import Q
	# queryset = Order.objects.all()
	serializer_class = OrderListStoreSerializer

	def get_queryset(self):
		
		non_store_user = Store.objects.filter(fk_user_id=self.request.user.id).first()
		settings.DPRINT(non_store_user)
		if non_store_user is None:
			# user_checkouts = UserCheckout.objects.filter(user_id=self.request.user.id).id
			# settings.DPRINT(user_checkouts.__dict__)
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
			# settings.DPRINT(user_checkouts.__dict__)
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
		settings.DPRINT(items)
		settings.DPRINT(cart.items.all())
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
		# settings.DPRINT(cart.items)
		# return Response(len(data))

	# queryset = Order.objects.all()

		# user_id = self.request.user.id
		# cart_id = 22
		# cart_items = CartItem.objects.all()
		# orders = Order.objects.filter(status=1, fk_ordered_store=1)
		# settings.DPRINT(orders.__dict__)
		# return orders




##Storewise_CART_ORDER_LIST 
class StoreWiseCartOrderLists(ListAPIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):

		order_id = request.GET.get('order_id', False) #fk_storewise_order_id passed here
		cart_items = CartItem.objects.filter(fk_storewise_order_id=order_id)
		# cart = Cart.objects.filter(id=cart_items)
		orders_list = []
		storewise_order = StoreWiseOrder.objects.filter(pk=order_id).first()
		settings.DPRINT('jpt')
		settings.DPRINT(storewise_order)
		remarks=""
		mobile=""
		status = False
		if storewise_order:
			mobile = storewise_order.fk_auth_user.mobile
			remarks = storewise_order.remarks
			status = storewise_order.is_cancelled
		


		# total_item = {len(cart_items)}
		items = CartItemSerializer(cart_items, many=True)
		# settings.DPRINT(items)
		cart = Cart()
		# settings.DPRINT(cart.items.all())
		data = {
		# "token": self.token,
		"cart" : cart.id,
		"total": cart.total,
		"subtotal": cart.subtotal,
		"tax_total": cart.tax_total,
		"mobile": mobile,
		"remarks": remarks,
		"cancel_status": status,
		"count": cart_items.count(),
		"items": items.data,
		# "product_id": items.id,
		}
		return Response(data)

		# # settings.DPRINT(total_item)
		# for item in cart_items:

		# 	data = {
		# 	"line_item_total": item.line_item_total,
		# 	"id": item.id,
		# 	"product_title": item.item.product.title,
		# 	"quantity": item.quantity,
		# 	"price": item.item.product.price,
		# 	"fk_storewise_order_id": item.fk_storewise_order_id

		# 	}
		# # 	settings.DPRINT(a)
		# # 	b = a.update(a)
		# # 	settings.DPRINT(b)

		# # return Response(b)
		# 	orders_list.append(data)
		# 	settings.DPRINT(orders_list)

		# return Response(orders_list)

	def get_queryset(self):
		return 
# 		alist = []
# for x in range(100):
#     adict = {1:x}
#     alist.append(adict)
# settings.DPRINT(alist)
		# settings.DPRINT(cart)

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


		# settings.DPRINT(cart.items)
		# return Response(len(data))

	# queryset = Order.objects.all()

		# user_id = self.request.user.id
		# cart_id = 22
		# cart_items = CartItem.objects.all()
		# orders = Order.objects.filter(status=1, fk_ordered_store=1)
		# settings.DPRINT(orders.__dict__)
		# return orders







# /api/api/create_order/
class CartOrderApiView(CreateAPIView):
	# permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset=Order.objects.all()
	serializer_class = CartOrderSerializer 


def UserOrderView(request):
	user_order_form = UserOrderForm()
	order_list = Order.objects.filter(status=1)
	# cart_items = Cart.cartitem_set.all()
	# settings.DPRINT(cart_items)

	return render(request, 'orders/user_order.html', {'user_order':user_order_form, 'order_list':order_list})


def UserOrderDetailView(request, id):
	cart_items = CartItem.objects.filter(cart_id=id)
	order = Order.objects.get(cart_id=id)
	cart = Cart.objects.get(id=id)

	total_price = order.shipping_total_price + cart.total
	# cart_item_list = cart_items.item
	# settings.DPRINT(cart_items.item)
	settings.DPRINT(cart_items.__dict__)
	return render(request, 'orders/order_detail.html', {'cart_items':cart_items, 'order':order, 'cart':cart, 'total_price':total_price})

	# return HttpResponse('User Order Detail View')

class UpdateOrderStatusApiView(CreateAPIView): ## YO USE BHAKO CHAINA //STOREWISE ORDER HAINA
	# permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset=Order.objects.all()
	serializer_class = UpdateOrderStatusSerializer

	def post(self, request):
		#import #psettings.DPRINT
		#psettings.DPRINT.#psettings.DPRINT(request.POST)
		order_id = request.POST.get('order_id')
		status = request.POST.get('status')
		settings.DPRINT(order_id)
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


from .fcm_service import send_fcm_token_for_device 
class UpdateStoreWiseOrderStatusApiView(CreateAPIView):
	# permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset=Order.objects.all()
	serializer_class = UpdateStoreWiseOrderStatusSerializer
	permission_classes = [permissions.IsAuthenticated]
	def post(self, request):

		# settings.DPRINT('jpt')
		settings.DPRINT(request.POST.get('order_id'))
		#psettings.DPRINT.#psettings.DPRINT(request.POST)
		storewiseorder_id = request.data.get('order_id') ### id of StoreWiseOrder model's.
		settings.DPRINT(storewiseorder_id)
		status = request.POST.get('status')
		# status = request.POST.get('returned')
		storewiseorder = StoreWiseOrder.objects.filter(pk=storewiseorder_id).first()
		user = User.objects.filter(pk=storewiseorder.fk_auth_user_id).first() #for user
		settings.DPRINT(user)
		if storewiseorder:
			# for storewise_order in storewiseorder:
			if status == "paid":
				storewiseorder.is_paid = True;

			if status == "transit":
				storewiseorder.is_transit = True;

			if status == "cancel":
				storewiseorder.is_cancelled = True;
				
			if status == "delivered":
				storewiseorder.is_delivered = True;
				is_depo=storewiseorder.fk_ordered_by_store_id is not None
				if is_depo:
					self.addProductinStore(storewiseorder) #DEPO LE COMPANY SANGA KINDA DEPO MA BADXA
				else:
					self.subProductinStore(storewiseorder) ###CUSTOMER LE DEPO SANGA KINDA KHERI GHATCHA

				#VariationHistoryCountService paxi garne bhaye
			storewiseorder.save()
			settings.DPRINT(status)
			send_fcm_token_for_device(settings.FCM_SERVER_KEY, user.firebase_token, storewiseorder.order_id, status)

			 # serverToken = settings.FCM_SERVER_KEY #server key here
  #deviceToken = user.firebase_token #'device token here'

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
				#import #psettings.DPRINT
				#psettings.DPRINT.#psettings.DPRINT(dict_buyer_product)
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



# from store.service import getUserStoreService
class myStoreName(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, *args, **kwargs):
		settings.DLFPRINT()
		settings.DPRINT(request.user.id)
		store = getUserStoreService(request.user.id)
		store_name=""
		if store:
			store_name = store.title
		# if not get_store_name:
		# 	store_user = StoreUser.objects.filter(fk_user_id=request.user.id).first()
		# 	store_id = get_store_name.fk_store_id
		# 	get_store_name = Store.objects.filter(fk_user_id=request.user.id).first()	
		# 	get_store_name = get_store_name.title
		return Response(store_name)


class AddNoteToOrderAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def post(self,request, *args, **kwargs):
		order_id = request.POST.get('order_id', False)
		if not order_id:
			return Response({"Fail": "We are unable to process your request"}, status.HTTP_400_BAD_REQUEST)
		order_note = request.POST.get('order_note', "")

		order = StoreWiseOrder.objects.filter(pk=order_id).first()
		if order:
			order.remarks = order_note
			order.save()
			return Response({
			'status': True,
			'detail': 'Note added'
		})

		else:
			return Response({"Fail": "We are unable to process your request"}, status.HTTP_400_BAD_REQUEST)

class CustomerCancelOrderAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def post(self,request, *args, **kwargs):
		order_id = request.data.get('order_id', None)
		# settings.DPRINT(order_id)
		user = request.user.id
		if not order_id:
			return Response({"Fail": "We are unable to process your request"}, status.HTTP_400_BAD_REQUEST)
		cancel_order = StoreWiseOrder.objects.filter(pk=order_id).first()
		if not cancel_order:
			return Response({"Fail": "We are unable to process your request"}, status.HTTP_400_BAD_REQUEST)
		if cancel_order.is_cancelled is True:
			return Response({"Fail": "Your order has already been cancelled"}, status.HTTP_400_BAD_REQUEST)
		else:

			if self.isOrderedTimeExpire(cancel_order.created_at):
				cancel_order.is_cancelled = True
				cancel_order.cancelled_at = datetime.now() 
				cancel_order.save()
				return Response({
				'status': True,
				'detail': 'Order Cancelled'
			})

			else:
				return Response({"Fail": "You can't cancel your order after 15 mintutes"}, status.HTTP_400_BAD_REQUEST)

	def isOrderedTimeExpire(self, order_created_at):
		current_time  = timezone.now() + timedelta(hours=5, minutes=45)
		settings.DPRINT('ordered time')
		settings.DPRINT(order_created_at+timedelta(hours=5, minutes=45))
		settings.DPRINT("current time")
		settings.DPRINT(current_time)
		time_difference  = current_time - (order_created_at+ timedelta(hours=5, minutes=45))
		dt = time_difference.total_seconds()
		# time = datetime.time(0, 15, 00, 000000).total_seconds()
		# settings.DPRINT(time)
		# settings.DPRINT(datetime.datetime(0, 15, 00, 000000).total_seconds())
		# settings.DPRINT(dt)
		settings.DPRINT('dt---')
		settings.DPRINT(dt)
		if dt <= 900:
			return True
		return False




def pos(request):
	context = {}
	return render(request, "personal/dashboard_layout/pos.html", context)

				
def pos1(request):
	cart = Cart.objects.filter(pk=request.GET.get('cart_id')).first()
	# print(cart_id)
	context = {
		# 'user_id' : patient_id
		"cart" : cart,
		'cart_id' : cart.id
	}
	return render(request, "personal/dashboard_layout/pos_test.html", context)


def cartitems(request):
	return pos1(request)

def carts(request):
	user_id = request.GET.get('user_id')
	visit_id = request.GET.get('visit_id')
	user = User.objects.filter(pk=user_id).first()
	if user_id:
		# user = User.objects.get(pk=user_id)
		carts = Cart.objects.order_by('-id').filter(user_id=user_id)
	if visit_id:
		carts = Cart.objects.order_by('-id').filter(fk_visit_id=visit_id)#(user_id=user_id)

	# print(cart_id)
	context = {
		'user_id' : user_id,
		'carts' : carts,
		'user' : user,
		"visit_id" : visit_id
		# 'cart_id' : cart_id.id
	}
	return render(request, "personal/dashboard_layout/carts.html", context)
	



###HMS

def visit(request):
	variations = Variation.objects.all()
	visits_type = TransactionType.objects.all()
	context ={
		'variations' : variations,
		'visits_type' : visits_type
	}
	return render(request, "personal/dashboard_layout/visit.html", context)