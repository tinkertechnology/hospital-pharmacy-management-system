from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .serializer import CreateUserSerializer, ProfileSerializer
from django.http import HttpResponse

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from blog.models import BlogPost
from django.contrib.auth.hashers import make_password
from .models import Account, PhoneOTP, PasswordResetOTP, CustomerRegisterSurvey, CustomerDepotRequest, CustomerMessage
from django.contrib.auth import get_user_model
import uuid
from django.shortcuts import get_object_or_404 
import random
import requests
from django.core.mail import send_mail
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

def privacy_policy(request):
	return render(request, 'account/privacy.html')


def login_view(request):
	print('login')
	# if request.method == 'POST':
	# 	mobile = request.POST.get('mobile')
	# 	password = request.POST.get('password')
	# 	print(mobile)
	# 	print(password)

	# 	user = authenticate(mobile=mobile, password=password)
	# 	print(user)

	# 	if user:
	# 		if user.is_active:
	# 			login(request, user)
	# 			return redirect('dashboard')
	# 		else:
	# 			return HttpResponse('Your account was inactive')
	# 	else:
	# 		return HttpResponse('Invalid login credentials')

	# return render(request, "account/login.html")
	
	context = {}

	user = request.user
	if user.is_authenticated: 
		print(1)
		return redirect('/dashboard')

	if request.POST:
		mobile = request.POST.get('mobile')
		password = request.POST.get('password')
		# print(mobile)
		# print(password)
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			print('passed')
			user = authenticate(mobile=mobile, password=password)

			if user:
				login(request, user)
				return redirect('dashboard')
		else:
			print('Failed')

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
			print(len(mobile))
			if len(mobile)!=10:
				return Response({"Fail": "Phone number length must be 10 digit"}, status.HTTP_400_BAD_REQUEST)

		
			user = Account.objects.filter(mobile__iexact=mobile)

			if user.exists():
				# return Response({
				# 	'status': False,
				# 	'detail': 'number already exists'
				# 	})
				return Response({"Fail": "Number already Exists"}, status.HTTP_400_BAD_REQUEST)
			else:
				key = send_otp(mobile)
				if key:
					old = PhoneOTP.objects.filter(mobile__iexact=mobile)
					if old.exists():
						old = old.first()
						count = old.count
						if count > 5:
							return Response({"Fail": "OTP sent limit, Please contact support"}, status.HTTP_400_BAD_REQUEST)
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
					data={'token' : settings.SPARROW_SMS_TOKEN,
					'from'  : settings.SMS_FROM,
					'to'    : mobile,
					'text'  : 'your mobile verification code is  ' + str(key)})

					status_code = r.status_code
					response = r.text
					response_json = r.json()
					print(status_code)
					print(response_json)
					print(key)
					# send_mail(
					# 'Thank you for your registration',
					# 'Your registered mobile nuymber is '+mobile+' .Use this OTP code for Verification. '+ str(key),
					# settings.EMAIL_HOST_USER,
					# ['sunilparajuli2002@gmail.com'],
					# #['gehendras52@gmail.com'],
					# fail_silently=False,
					# )
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
			return Response({"Fail": "Please enter phone number to continue"}, status.HTTP_400_BAD_REQUEST)



def send_otp(mobile):
	if mobile:
		key = random.randint(111111, 999999)
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
					return Response({"Fail": "Incorrect OTP Code please try again"}, status.HTTP_400_BAD_REQUEST)
			else:
				return Response({"Fail": "First proceed with OTP verification"}, status.HTTP_400_BAD_REQUEST)


		else:
			return Response({"Fail": "Please both OTP code and mobile number"}, status.HTTP_400_BAD_REQUEST)


class RegisterAPI(APIView):

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		print('first')
		mobile = request.data.get('mobile', False)
		password = request.data.get('password', False)
		email = request.data.get('email', False)
		username = mobile
		firstname = request.data.get('firstname')
		lastname = request.data.get('lastname')
		# if firstname and lastname:
		# 	return Response({"Fail": "Please enter your firstname and lastname"}, status.HTTP_400_BAD_REQUEST)

		if mobile and password:	
			if len(mobile)!=10:
				return Response({"Fail": "Please check your mobile number, it should be 10 digit"}, status.HTTP_400_BAD_REQUEST)

			old = PhoneOTP.objects.filter(mobile__iexact=mobile)
			if old.exists():
				old = old.first()
				validated = old.validated

				if validated:
					temp_data = {
						'mobile': mobile,
						'password': password,
						'email': email,
						'username': mobile,
						'firstname': firstname,
						'lastname':lastname

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
					return Response({"Fail": "OTP havent verified first , first validate otp"}, status.HTTP_400_BAD_REQUEST)
				

			else:
				return Response({"Fail": "Please Verify your phone first through OTP"}, status.HTTP_400_BAD_REQUEST)

		else:
			return Response({"Fail": "Please, enter mobile and password "}, status.HTTP_400_BAD_REQUEST)







class ResetPasswordAPIView(APIView):
	def post(self, request, *args, **kwargs):
		mobile = request.data.get('mobile', False)
		print(1)
		if mobile:
			print(2)
			print(len(mobile))

			if len(mobile)!=10:
				print(3)
				return Response({"Fail": "Please enter 10 digit phone number"}, status.HTTP_400_BAD_REQUEST)

			old = User.objects.filter(mobile__iexact=mobile).first()
			if  old is not None:#old.exists():
				print(4)
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
				# print(old.mobile)
				old.password = make_password(new_password)
				old.save()
				r = requests.post(
				"http://api.sparrowsms.com/v2/sms/",
				data={'token' : settings.SPARROW_SMS_TOKEN,
				'from'  : settings.SMS_FROM,
				'to'    : mobile,
				'text'  : 'your new password is  '+new_password})

				status_code = r.status_code
				response = r.text
				response_json = r.json()
				print(status_code)
				print(response_json)
				# send_mail(
				# 	'A reset password has been sent',
				# 	'A reset password has been sent to your mobile number '+ mobile + '. Use this '+new_password+ ' code for login',
				# 	settings.EMAIL_HOST_USER,
				# 	['sunilparajuli2002@gmail.com'],
				# 	#['gehendras52@gmail.com'],
				# 	fail_silently=False,
				# 	)

				# user = serializer.save()
				return Response({
					'status': True,
					'detail': 'Password has been sent to your mobile '+ new_password
					})
			else:
				return Response({"Fail": "The Mobile number was not found"}, status.HTTP_400_BAD_REQUEST)

		else:
			return Response({"Fail": "Please enter phone number to continue"}, status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
	# permission_classes = [IsAuthenticated]
	def post(self, request, *args, **kwargs):
		user = request.user
		user_db = User.objects.get(pk=user.id)
		new_password = request.data.get('new_password')
		old_password = request.data.get('old_password')
		confirm_new_password = request.data.get('confirm_new_password')
		print(user.mobile)
		print(request.data)
		if new_password and confirm_new_password:
			if new_password!=confirm_new_password:
				return Response({"Fail": "The two password fields must match."}, status.HTTP_400_BAD_REQUEST)

		if new_password and old_password:
			print(old_password)
			# check_old_password = user.check_password(old_password)
			check_old_password = authenticate(mobile=str(user.mobile), password=str(old_password))
			print(check_old_password)
			if not check_old_password:
				return Response({"Fail": "Your previous password doesn't match, please try again"}, status.HTTP_400_BAD_REQUEST)
						
			print(user.mobile)
			user_db.password = make_password(new_password)
			user_db.save()
		# user = serializer.save()
			return Response({
				'status': True,
				'detail': 'Password has been changed !' + new_password
				})
			
		else:
			return Response({"Fail": "Please input desired password and try again"}, status.HTTP_400_BAD_REQUEST)


class PasswordResetSendOTP(APIView):
	def post(self, request, *args, **kwargs):
		phone_number = request.data.get('mobile')
		if phone_number:
			mobile = str(phone_number)
			print(len(mobile))
			if len(mobile) != 10:
				return Response({"Fail": "Phone number length must be 10 digit"}, status.HTTP_400_BAD_REQUEST)

			user = Account.objects.filter(mobile__iexact=mobile)

			if not user.exists():
				# return Response({
				# 	'status': False,
				# 	'detail': 'number already exists'
				# 	})
				return Response({"Fail": "Number doesn't already Exists, please register"}, status.HTTP_400_BAD_REQUEST)
			else:
				key = send_otp(mobile)
				if key:
					old = PasswordResetOTP.objects.filter(mobile__iexact=mobile)
					if old.exists():
						old = old.first()
						count = old.count
						if count > 2:
							return Response({"Fail": "OTP sent limit, Please contact support"},
											status.HTTP_400_BAD_REQUEST)
						old.count = count + 1
						old.otp = key
						old.save()
						print('increaded count', count)
					else:
						PasswordResetOTP.objects.create(
							mobile=mobile,
							otp=key,
						)
					r = requests.post(
						"http://api.sparrowsms.com/v2/sms/",
						data={'token': settings.SPARROW_SMS_TOKEN,
							  'from': settings.SMS_FROM,
							  'to': mobile,
							  'text': 'your password reset OTP code is  ' + str(key)})
					
					status_code = r.status_code
					response = r.text
					response_json = r.json()
					print(status_code)
					print(response_json)
					print(key)
					# send_mail(
					# 'Thank you for your registration',
					# 'Your registered mobile nuymber is '+mobile+' .Use this OTP code for Verification. '+ str(key),
					# settings.EMAIL_HOST_USER,
					# ['sunilparajuli2002@gmail.com'],
					# #['gehendras52@gmail.com'],
					# fail_silently=False,
					# )
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
			return Response({"Fail": "Please enter phone number to continue"}, status.HTTP_400_BAD_REQUEST)


class ValidateResetPasswordOTP(APIView):
	def post(self, request, *args, **kwargs):
		mobile = request.data.get('mobile', False)
		otp_sent = request.data.get('otp', False)
		print(request.data)
		if mobile and otp_sent:
			old = PasswordResetOTP.objects.filter(mobile__iexact=mobile)
			if old.exists():
				print(1)
				old = old.first()
				otp = old.otp
				if(str(otp_sent)==str(otp)):
					old.validated = True
					old.otp = "999234234"
					old.save()
					return Response({
						'status': True,
						'detail': 'OTP matched, enter your new credentials'
						})

				else:
					# otp.validated = False
					# otp.save()
					return Response({"Fail": "Incorrect OTP Code please try again"}, status.HTTP_400_BAD_REQUEST)
			else:
				return Response({"Fail": "First proceed with OTP verification"}, status.HTTP_400_BAD_REQUEST)


		else:
			return Response({"Fail": "Please enter both OTP code and mobile number"}, status.HTTP_400_BAD_REQUEST)


class ChangePasswordAfterOtpAPIView(APIView):
	# permission_classes = [IsAuthenticated]
	def post(self, request, *args, **kwargs):
		print(request.data)
		mobile = request.data.get('mobile', False)
		new_password = request.data.get('new_password', False)
		confirm_new_password = request.data.get('confirm_new_password', False)
		# verified = PasswordResetOTP.objects.filter(mobile=mobile)
		# if verified.validated==True:
		user = User.objects.get(mobile=mobile)
		user_db = User.objects.get(pk=user.id)
		print(user.mobile)
		print(request.data)
		if new_password and confirm_new_password:
			if new_password != confirm_new_password:
				return Response({"Fail": "The two password fields must match."}, status.HTTP_400_BAD_REQUEST)
			print(user.mobile)
			user_db.password = make_password(new_password)
			user_db.save()
			# user = serializer.save()
			return Response({
				'status': True,
				'detail': 'Password has been changed !'
			})

		else:
			return Response({"Fail": "Please input desired password and try again"}, status.HTTP_400_BAD_REQUEST)
	# else:
	# 	return Response({"Fail": "Your otp hasn't been verified yet, try again"}, status.HTTP_400_BAD_REQUEST)
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class CustomerRegisterSurveyAPIView(APIView):
	def post(self, request, *args, **kwargs):
		print(request.data)
		mobile = request.data.get('mobile', False)
		name = request.data.get('name', False)
		location = request.data.get('location', False)
		email = request.data.get('email', False)
		try:
			validate_email(email.strip())
		except:
			return Response({"Fail": "Incorrect email format, please try again"}, status.HTTP_400_BAD_REQUEST)

		# if not valid_email:
		# 	return Response({"Fail": "Email format is incorrect, please input correct email address"}, status.HTTP_400_BAD_REQUEST)
		know_about_us = request.data.get('know_about_us', False)
		other = request.data.get('other', False)
		if not mobile:
			return Response({"Fail": "Mobile number required"}, status.HTTP_400_BAD_REQUEST)
		if len(mobile)<10:
			return Response({"Fail": "Mobile number must be 10 digits"}, status.HTTP_400_BAD_REQUEST)
		if not name:
			return Response({"Fail": "Full name is required"}, status.HTTP_400_BAD_REQUEST)
		if not location:
			return Response({"Fail": "Location is required"}, status.HTTP_400_BAD_REQUEST)
		if not email:
			return Response({"Fail": "Your email is required"}, status.HTTP_400_BAD_REQUEST)
		if not know_about_us:
			return Response({"Fail": "let us know how you know about us"}, status.HTTP_400_BAD_REQUEST)
		if not other:
			return Response({"Fail": "Message is required"}, status.HTTP_400_BAD_REQUEST)
		
		survey_data = CustomerRegisterSurvey()
		survey_data.mobile = mobile
		survey_data.name = name
		survey_data.location = location
		survey_data.email = email
		survey_data.know_about_us = know_about_us
		survey_data.other = other
		survey_data.save()

		send_mail(
		    'Survey Notification',
		    'Name:'+ name + ' mobile:'+mobile + ' location: '+location 
		    	+ 'i know sarovara by: '+know_about_us + ' other: '+other ,
		    [email],
		    [settings.EMAIL_HOST_USER],
		    fail_silently=False,
		)
		return Response({
			'status': True,
			'detail': 'Thank you for your time'
		})


class CustomerMessageForDepotAPIView(APIView):
	def post(self, request, *args, **kwargs):
		print(request.data)
		mobile = request.data.get('mobile', None)
		name = request.data.get('name', None)
		location = request.data.get('location', None)
		message = request.data.get('message', None)

		if not mobile:
			return Response({"Fail": "Mobile number required"}, status.HTTP_400_BAD_REQUEST)
		if len(mobile) < 10:
			return Response({"Fail": "Mobile number must be 10 digits"}, status.HTTP_400_BAD_REQUEST)
		if not name:
			return Response({"Fail": "Full name is required"}, status.HTTP_400_BAD_REQUEST)
		if not location:
			return Response({"Fail": "Location is required"}, status.HTTP_400_BAD_REQUEST)
		if not message:
			return Response({"Fail": "Your Message is required"}, status.HTTP_400_BAD_REQUEST)

		depot_request = CustomerDepotRequest()
		depot_request.mobile = mobile
		depot_request.name = name
		depot_request.location = location
		depot_request.message = message
		depot_request.save()

		send_mail(
			'Request for depot',
			'Name:' + name + ' mobile:' + mobile + ' location: ' + location
			 + ' Message: ' + message,
			[settings.EMAIL_HOST_USER],
			[settings.EMAIL_HOST_USER],
			fail_silently=False,
		)
		return Response({
			'status': True,
			'detail': 'Thank you for your time'
		})



class CustomerMessageAPIView(APIView):
	def post(self, request, *args, **kwargs):
		print(request.data)
		message = request.data.get('message', None)
		if not message:
			return Response({"Fail": "Your Message is required"}, status.HTTP_400_BAD_REQUEST)

		customer_message = CustomerMessage()
		customer_message.message = message
		customer_message.save()

		send_mail(
			'Customer Message',
			  ' Message : ' + str(message),
			settings.EMAIL_HOST_USER,
			[settings.EMAIL_HOST_USER],
			fail_silently=False,
		)
		return Response({
			'status': True,
			'detail': 'Thank you for your Message'
		})
