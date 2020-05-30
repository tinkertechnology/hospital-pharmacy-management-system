from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializer import CreateUserSerializer
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from blog.models import BlogPost
from django.contrib.auth.hashers import make_password
from .models import Account, PhoneOTP
from django.contrib.auth import get_user_model
import uuid
from django.shortcuts import get_object_or_404 
import random
import requests
User = get_user_model()

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')


def login_view(request):
	
	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)

def account_jpt(view):
	return render(request, "jpt.html")

def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
				}
			)

	context['account_form'] = form

	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts

	return render(request, "account/account.html", context)


def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})


class ValidatePhoneSendOTP(APIView):

	def post(self, request, *args, **kwargs):
		phone_number = request.data.get('mobile')
		if phone_number:
			mobile = str(phone_number)
		
			user = Account.objects.filter(mobile__iexact=mobile)

			if user.exists():
				return Response({
					'status': False,
					'detail': 'number already exists'
					})
			else:
				key = send_otp(mobile)
				if key:
					old = PhoneOTP.objects.filter(mobile__iexact=mobile)
					if old.exists():
						old = old.first()
						count = old.count
						if count > 10:
							return Response({
								'status': False,
								'detail': 'OTP limit exists, contact support'
								})
						old.count = count + 1
						old.otp = key
						old.save()
						print('increaded count', count)
					else:
						PhoneOTP.objects.create(
							mobile = mobile,
							otp = key,
							)
					r = requests.post(
					"http://api.sparrowsms.com/v2/sms/",
					data={'token' : 'ZkikH0ihw90CzvR2yAOn',
					'from'  : 'Demo',
					'to'    : '1234567890',
					'text'  : 'your mobile verification code is  ' + str(key)})

					status_code = r.status_code
					response = r.text
					response_json = r.json()
					print(status_code)
					print(response_json)
					
					return Response({
						'status': True,
						'detail': 'OTP sent to ' + mobile
						})
				else:
					return Response({
						'status': False,
						'detail': 'error sending OTP'
						})
		else:
			return Response({
				'status': False,
				'detail': 'mobile number not given'

				})



def send_otp(mobile):
	if mobile:
		key = random.randint(999, 9999)
		print(key)
		return key
	else :
		return False




class ValidateOTP(APIView):
	def post(self, request, *args, **kwargs):
		mobile = request.data.get('mobile', False)
		otp_sent = request.data.get('otp', False)

		if mobile and otp_sent:
			old = PhoneOTP.objects.filter(mobile__iexact=mobile)
			if old.exists():
				old = old.first()
				otp = old.otp
				if(str(otp_sent)==str(otp)):
					old.validated = True
					old.save()
					return Response({
						'status': True,
						'detail': 'OTP matched, proceed for registration'
						})


				else:
					return Response({
						'status': False,
						'detail': 'Incorrect OTP'
						})
			else:
				return Response({
					'status' : False,
					'detail' : 'First proceed via sending OTP request'
					})


		else:
			return Response({
				'status': False,
				'detail': 'Please provide both phone number and OTP for validation'
				})


class RegisterAPI(APIView):

	print('inside register view')
	@csrf_exempt
	def post(self, request, *args, **kwargs):
		print('first')
		mobile = request.data.get('mobile', False)
		password = request.data.get('password', False)
		email = request.data.get('email', False)
		username = mobile
		if mobile and password:
			
			old = PhoneOTP.objects.filter(mobile__iexact=mobile)
			if old.exists():
				old = old.first()
				validated = old.validated

				if validated:
					temp_data = {
						'mobile': mobile,
						'password': password,
						'email': email,
						'username': mobile

					}
					serializer = CreateUserSerializer(data = temp_data)
					serializer.is_valid(raise_exception = True)
					user = serializer.save()
					old.delete()

					return Response({
						'status': True,
						'detail': 'Account Created'
						})

				else:
					return Response({
						'status': False,
						'detail': 'OTP havent verified first , first validate otp'
						})

			else:
				return Response({
						'status': False,
						'detail': 'Please Verify your phone first through OTP'
					})

		else:
			return Response({
				'status': False,
				'detail': 'Both phone and password are not sent'
				})




class ResetPasswordAPIView(APIView):
	def post(self, request, *args, **kwargs):
		mobile = request.data.get('mobile', False)
		if mobile:
			old = User.objects.filter(mobile__iexact=mobile).first()
			print(old.__dict__)
			if  old is not None:#old.exists():
				new_password = uuid.uuid4().hex[:6].upper()
				# print(new_password)
				# temp_data = {
				# 	'mobile': old.mobile,
				# 	'email': old.email,
				# 	'username': old.username,
				# 	'password': new_password
				# }
				# serializer = UpdateUserSerializer(data = temp_data)
				# serializer.is_valid(raise_exception = True)
				old.password = make_password(new_password)
				old.save()
				# user = serializer.save()
				return Response({
					'status': True,
					'detail': 'Password has been sent to your mobile '+ new_password
					})
			else:
				return Response({
					'status': False,
					'detail': 'mobile number hasnt been registered yet'

					})

		else:
			return Response({
				'status': False,
				'detail' : 'Mobile number was not given'
				})





