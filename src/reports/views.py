from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
# Create your views here.

# from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

### import models for report here ####
from orders.models import *

from datetime import datetime, timedelta, time
from django.utils.dateparse import parse_date
import dateutil.parser
from .serializers import ReportSerializer
from django.db.models.functions import TruncDate
from django.db.models import Sum, F
from django.db.models.expressions import RawSQL
from rest_framework.response import Response

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

