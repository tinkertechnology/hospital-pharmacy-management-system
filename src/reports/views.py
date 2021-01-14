from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
# Create your views here.
# from rest_framework import serializers
from django.core import serializers
# from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

### import models for report here ####
from orders.models import *

from datetime import datetime, timedelta, time
from django.utils.dateparse import parse_date
# import dateutil.parser
from .serializers import ReportSerializer
from django.db.models.functions import TruncDate
from django.db.models import Sum, F
from django.db.models.expressions import RawSQL
from rest_framework.response import Response
import json
import datetime

# Create your views here.


class DailySalesApiView(ListAPIView):
	serializer_class = ReportSerializer
	# def post(self, request, *args, **kwargs):
	def get_queryset(self):
		parameter = self.request.data
		# to_date = self.request.GET.get('to_date')
		date1 = '2020-06-17 00:00:00';
		date2 = '2020-06-18 00:00:00';
		from_date = dateutil.parser.parse(date1)
		to_date = dateutil.parser.parse(date2)
		# to_date = '2020-07-19 00:00:00';
		# qs =  StoreWiseOrder.objects.annotate(created_at_date=RawSQL("date(created_at)", ())).values('created_at_date').annotate(order_total_sum=Sum('order_total'))
		qs =  StoreWiseOrder.objects.annotate(a=RawSQL("date(created_at)", ()),
			o=Sum('order_total')).values('a')
		# StoreWiseOrder.objects.annotate(created_at_date=TruncDate('created_at')).values('created_at_date').aggregate(Sum('order_total'))
		# print(qs.query)
		print(qs.query)

		return qs
	# 	qs = qs.filter(created_at__gte=from_date)

from django.db import connection, transaction
# class UserCountProductWiseReport(ListAPIView):
# 	def get_context_data(self, **kwargs):
# 		cursor = connection.cursor()
# 		cursor.execute("""with accountVariationQuantity as (
# select 
# account_account.id as account_id, products_variation.id as variation_id, sum(quantity) as product_quantity
# from orders_storewiseorder 
# left join account_account on orders_storewiseorder.fk_auth_user_id = account_account.id 
# left join carts_cart on  orders_storewiseorder.cart_id = carts_cart.id
# left join carts_cartitem on carts_cartitem.cart_id = carts_cart.id
# left JOIN products_variation on products_variation.id = carts_cartitem.item_id
# left join products_product on products_variation.product_id = products_product.id
# left join orders_usercheckout on orders_usercheckout.user_id = account_account.id
# left join orders_useraddress on orders_useraddress.user_id = orders_usercheckout.user_id
# group by account_account.id, products_variation.id
# )
# select firstname, lastname, mobile, products_product.title, products_variation.title, avq.product_quantity
# from accountVariationQuantity avq
# inner join account_account on avq.account_id = account_account.id
# inner join products_variation on avq.variation_id = products_variation.id
# left join products_product on products_variation.product_id = products_product.id
# order by avq.product_quantity DESC
# ;""");
# 		row = cursor.fetchall()
# 		print(row)
# 		data = {
# 		'count': len(row),
# 		'data': row
# 		}
# 		context['results'] = data
# 		return context


# def duplicatephoneno(request):
#     payload = json.loads(request.body.decode('utf-8'))
#     print(payload)

#     if payload:
#         startdate=payload['from']
#         enddate=payload['to']
#         with connection.cursor() as cursor:

#             queries="SELECT * FROM `allergy` WHERE `allergy`.`patient_n_key` IN (SELECT `patient_masters`.`patient_n_key` FROM `patient_masters` WHERE `patient_masters`.`created_on`between %s AND %s)"
#             data_tuple=(startdate,enddate)
#             cursor.execute(queries,data_tuple)
#             connection.commit()
#             row = cursor.fetchall()
#             patientuser=serializers.serialize('json', row)
#             return HttpResponse(patientuser, content_type='application/json;charset=utf8')



def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
	dict(zip(columns, row))
	for row in cursor.fetchall()
	]

def GetJsonFromQueryData(query):
	cursor = connection.cursor()
	cursor.execute(query);
	# connection.commit()

	data = json.dumps(dictfetchall(cursor), default=myconverter)
	return data
	# patientuser=serializers.serialize('json', row)
	# return HttpResponse(data, content_type='application/json;charset=utf8')

def UserCountProductWiseReport(self):
	cursor = connection.cursor()
	cursor.execute("""with accountVariationQuantity as (
		select 
		account_account.id as account_id, products_variation.id as variation_id, sum(quantity) as product_quantity
		from orders_storewiseorder 
		left join account_account on orders_storewiseorder.fk_auth_user_id = account_account.id 
		left join carts_cart on  orders_storewiseorder.cart_id = carts_cart.id
		left join carts_cartitem on carts_cartitem.cart_id = carts_cart.id
		left JOIN products_variation on products_variation.id = carts_cartitem.item_id
		left join products_product on products_variation.product_id = products_product.id
		left join orders_usercheckout on orders_usercheckout.user_id = account_account.id
		left join orders_useraddress on orders_useraddress.user_id = orders_usercheckout.user_id
		group by account_account.id, products_variation.id
		)
		select firstname, lastname, mobile, products_product.title, products_variation.title, avq.product_quantity
		from accountVariationQuantity avq
		inner join account_account on avq.account_id = account_account.id
		inner join products_variation on avq.variation_id = products_variation.id
		left join products_product on products_variation.product_id = products_product.id
		order by avq.product_quantity DESC
		;""");
	# connection.commit()

	data = json.dumps(dictfetchall(cursor))
	# patientuser=serializers.serialize('json', row)
	return HttpResponse(data, content_type='application/json;charset=utf8')


def UserWithoutPurchaseReport(self):
	query = """ select 
		firstname, lastname, mobile
		from orders_storewiseorder 
		right join account_account on orders_storewiseorder.fk_auth_user_id = account_account.id 
		where orders_storewiseorder.id is null;
		"""

	data = GetJsonFromQueryData(query)
	return HttpResponse(data, content_type='application/json;charset=utf8')


def UserOrderDetailReport(self):
	query = """ select 
firstname, lastname,mobile, state,city, street, products_product.title,products_variation.title,quantity,
created_at, order_latitude, order_longitude
from orders_storewiseorder 
left join account_account on orders_storewiseorder.fk_auth_user_id = account_account.id 
left join carts_cart on  orders_storewiseorder.cart_id = carts_cart.id
left join carts_cartitem on carts_cartitem.cart_id = carts_cart.id
left JOIN products_variation on products_variation.id = carts_cartitem.item_id
left join products_product on products_variation.product_id = products_product.id
left join orders_usercheckout on orders_usercheckout.user_id = account_account.id
left join orders_useraddress on orders_useraddress.user_id = orders_usercheckout.user_id
;"""

	data = GetJsonFromQueryData(query)
	return HttpResponse(data, content_type='application/json;charset=utf8')

from carts.models import *
from orders.serializers import StoreWiseOrderSerializer
from carts.serializers import CartSeriailzer
from datetime import datetime as dt
from products.models import UserVariationQuantityHistory
# import datetime
class SalesAndCreditReportByDeliveryBoy(APIView):
	def get(self, request, *args, **kwargs):
		date = request.GET.get('date')
		datetime_object = dt.now() #dt.strptime(date, '%Y-%m-%d')
		if date:
			datetime_object = dt.strptime(date, '%Y-%m-%d')
		print(datetime_object)
		print(dt.now())
		delivery_boy_id = request.GET.get('delivery_boy_id')
		print(delivery_boy_id)
		store_id = request.GET.get('store_id')
		#qs = StoreWiseOrder.objects.filter(created_at__contains=dt.date(date))
		qs = Cart.objects.filter(timestamp__contains=dt.date(datetime_object)) #dt.date(date))
		if delivery_boy_id:
			qs = qs.filter(fk_delivery_user_id=delivery_boy_id)
		total_sales = qs.aggregate(total_price=Sum('total')) 
		credit = qs.aggregate(total_credit=Sum('credit')) 
		debit = qs.aggregate(total_debit=Sum('debit')) 
		qs_jar = UserVariationQuantityHistory.objects.filter(timestamp__contains=dt.date(datetime_object))
		total_jars_hold = qs_jar.aggregate(total_jars_hold=Sum('num_delta'))
		# if store_id:
		# 	order_id = StoreWiseOrder.objects.filter()
		# 	qs = qs.filter()
		data = dict()
		serializers = CartSeriailzer(qs, many=True)
		data = {
			'total_sales':total_sales,
			'credit' : credit,
			'debit' : debit,
			'jars_hold' : total_jars_hold,
			"count": qs.count(),
			'data': serializers.data
		}
		return Response(data)
		# if delivery_boy_id:
			# pass



