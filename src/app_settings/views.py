from django.shortcuts import render

# Create your views here.
from .models import AppSettings

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# from .serializer import CreateUserSerializer
from django.http import HttpResponse
from django.views.generic import TemplateView, View, FormView, ListView, DetailView


from django.contrib.auth import get_user_model
import uuid
from django.shortcuts import get_object_or_404 
import random
import requests
from django.core.mail import send_mail
#from .services import GetGuestCartSessionId


class AppSettingsAPIView(APIView):
	def get(self, request):
		return Response("1");
		# guestcart = GuestCart()
		phone_number = request.data.get('phone_number')
		email = request.data.get('email')
		if not phone_number:
			return Response({"Fail": "Phone number must be provided"}, status.HTTP_400_BAD_REQUEST)

		if not email:
			return Response({"Fail": "Email must be provided"}, status.HTTP_400_BAD_REQUEST)		
		session_id = GetGuestCartSessionId(request)
		guestcarts = GuestCart.objects.filter(session_id=session_id)
		for guestcart in guestcarts:
			guestcart.email = email
			guestcart.phone_number = phone_number
			guestcart.is_confirmed = True
			guestcart.save()
		return Response({
			'status': True,
			'detail': 'Confirmed order'
			})


class MobileAppVersion(APIView):
	def get(self, request):
		return Response("1");

