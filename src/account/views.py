from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .serializer import CreateUserSerializer, ProfileSerializer #, SurveyRegisterSerializer
from django.http import HttpResponse
from .serializer import PatientSerializer
from users.models import UserType
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.contrib.auth.hashers import make_password
from .models import Account, PhoneOTP, PasswordResetOTP #FsurvgisterSurvey, CustomerDepotRequest, CustomerMessage
from django.contrib.auth import get_user_model
import uuid
from django.shortcuts import get_object_or_404 
import random
import requests
from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView, ListAPIView
from store.models import StoreUser #., StoreAccount, 
from .serializer import UserSerializer#, CallLogSerializer
from django.http import Http404
from django.db.models import Count, Max, Min, Avg
from carts.models import CartItem, Cart
from carts.service import CartItemCreateService
from orders.service import CreateOrderFromCart
from orders.constants import ORDER_TYPE_MISSCALL
import datetime
from django.utils import timezone
from counter.models import Counter
from users.models import UserTypes
from .models import Visit, VisitType
from datetime import datetime as dt, timedelta
from django.core.paginator import Paginator
from django.contrib import messages

User = get_user_model()

def registration_view(request):
	settings.DLFPRINT()
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
		context['counters'] = Counter.objects.all()
	return render(request, 'account/register.html', context)


def logout_view(request):
	settings.DLFPRINT()
	logout(request)
	return redirect('/')

def privacy_policy(request):
	settings.DLFPRINT()
	return render(request, 'account/privacy.html')


def login_view(request):
	settings.DLFPRINT()
	print('login')
	context = {'counters' : Counter.objects.all()}

	user = request.user
	if user.is_authenticated: 
		return redirect('/dashboard')

	if request.POST:
		mobile = request.POST.get('mobile')
		password = request.POST.get('password')
		# print(mobile)
		# print(password)
		print(request.POST)
		form = AccountAuthenticationForm(request.POST)
		# if form.is_valid():
		request.session['counter'] = request.POST.get('counter')
		print('session counter',request.session.get('counter'))
		user = authenticate(mobile=mobile, password=password)
		print(user)
		if user:
			login(request, user)
			return redirect('dashboard')
		else:
			print('Failed')

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	context['visits'] = Counter.objects.all()
	

	# print(form)
	return render(request, "account/login.html", context)


def account_view(request):
	settings.DLFPRINT()
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
	settings.DLFPRINT()
	return render(request, 'account/must_authenticate.html', {})


class ValidatePhoneSendOTP(APIView):

	def post(self, request, *args, **kwargs):
		settings.DLFPRINT()
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
	settings.DLFPRINT()
	if mobile:
		key = random.randint(111111, 999999)
		print(key)
		return key
	else :
		return False





class ValidateOTP(APIView):
	def post(self, request, *args, **kwargs):
		settings.DLFPRINT()
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

from datetime import datetime
class RegisterAPI(APIView):

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		settings.DLFPRINT()
		print(request.data)
		mobile = request.data.get('mobile', False)
		# password = request.data.get('password', False)
		password = mobile
		email = request.data.get('email', False)
		username = mobile
		firstname = request.data.get('firstname')
		lastname = request.data.get('lastname')
		patient_type = request.data.get('patient_type')
		date_of_birth = request.data.get('date_of_birth')
		emergency_number = request.data.get('emergency_number')
		fk_blood_id = request.data.get('fk_bloodgroup_id')
		if date_of_birth:
			date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
		
		if mobile and password:	
			if len(mobile)!=10:
				return Response({"Fail": "Please check your mobile number, it should be 10 digit"}, status.HTTP_400_BAD_REQUEST)
			temp_data = {
						'mobile': mobile,
						'password': password,
						'email': email,
						'username': mobile,
						'firstname': firstname,
						'lastname':lastname,
						'date_of_birth': date_of_birth,
						'fk_blood_id' : 1,
						'fk_country_id' : 1,
						'emergency_number' : emergency_number,

					}
			serializer = CreateUserSerializer(data = temp_data)
			serializer.is_valid(raise_exception = True)
			user = serializer.save()
			##saving the created user as patient 
			## only save if usertype is selected from form
			if request.data.get('patient_type_id'):
				usertype = UserType()
				usertype.user_id = user.id
				usertype.user_type_id = request.data.get('patient_type_id')
				usertype.save() 
			data = {}
			return Response({
				'status': True,
				'detail': 'Account Created',
				'user_id' : user.id
				})

			old = PhoneOTP.objects.filter(mobile__iexact=mobile)
			if old.exists():
				old = old.first()
				validated = old.validated

				if validated:
					pass
					

				else:
					return Response({"Fail": "OTP havent verified first , first validate otp"}, status.HTTP_400_BAD_REQUEST)
				

			else:
				return Response({"Fail": "Please Verify your phone first through OTP"}, status.HTTP_400_BAD_REQUEST)

		else:
			return Response({"Fail": "Please, enter mobile and password "}, status.HTTP_400_BAD_REQUEST)







class ResetPasswordAPIView(APIView):
	def post(self, request, *args, **kwargs):
		settings.DLFPRINT()
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
		settings.DLFPRINT()
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
				'detail': 'Password has been changed !'
				})
			
		else:
			return Response({"Fail": "Please input desired password and try again"}, status.HTTP_400_BAD_REQUEST)


class PasswordResetSendOTP(APIView):
	def post(self, request, *args, **kwargs):
		settings.DLFPRINT()
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
		settings.DLFPRINT()
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
		settings.DLFPRINT()
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



class CustomerMessageForDepotAPIView(APIView):
	def post(self, request, *args, **kwargs):
		settings.DLFPRINT()
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
		settings.DLFPRINT()
		print(request.data)
		message = request.data.get('message', None)
		phone = request.data.get('phone', None)
		if not message:
			return Response({"Fail": "Your Message is required"}, status.HTTP_400_BAD_REQUEST)
		if not phone:
			return Response({"Fail": "Your Phone number is required"}, status.HTTP_400_BAD_REQUEST)

		customer_message = CustomerMessage()
		customer_message.message = message
		customer_message.save()

		send_mail(

			'Customer Message',
			' Phone : ' + str(phone)+ ' '+
			  ' Message : ' + str(message),
			settings.EMAIL_HOST_USER,
			[settings.EMAIL_HOST_USER],
			fail_silently=False,
		)
		return Response({
			'status': True,
			'detail': 'Thank you for your Message'
		})


class CheckTokenAPIView(APIView):
	#authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		data = {
			"success": True,

			# "product_id": items.id,
		}
		# print(cart.items)
		return Response(data)

from .sms_service import send_sms_to_phone

class SendMessageToMobileAPIView(APIView):
	def post(self, request, *args, **kwargs):
		settings.DLFPRINT()
		mobile = request.data.get('mobile')
		message = request.data.get('message')
		r = requests.post(
        "http://api.sparrowsms.com/v2/sms/",
        data={'token' : settings.SPARROW_SMS_TOKEN,
        'from'  : settings.SMS_FROM,
        'to'    : mobile,
        'text'  : message })

		status_code = r.status_code
		response = r.text
		response_json = r.json()
		print(status_code)
		print(response_json)
		print(mobile)
		print(message)
		if status_code==200:
			return Response({
				'status': True,
				'detail': 'SMS sent to' + mobile
			})
	
		return Response({"Fail": "SMS was not sent"}, status.HTTP_400_BAD_REQUEST)


class SaveUpdateFirebaseToken(APIView):
	def post(self, request, *args, **kwargs):
		settings.DLFPRINT()
		firebase_token = request.data.get('firebase_token')
		user = User.objects.filter(pk=request.user.id).first()
		user.firebase_token = firebase_token
		user.save()
		return Response({
				'status': True,
				'detail': 'updated firebasetoken'
			})


from products.models import UserVariationQuantityHistory
from products.serializers import UserVariationQuantityHistorySerializer
class GetUserJarAndCreditAPIView(APIView):
	serializer_class = UserVariationQuantityHistorySerializer
	def post(self, request, *args, **kwargs):
		settings.DLFPRINT()
		phone = request.data.get('phone')
		print(phone)
		if phone:
			user = Account.objects.filter(mobile__iexact=phone).first()
			if not user:
				return Response({"Fail": phone+ " is not registered, please register"}, status.HTTP_400_BAD_REQUEST)
			data = dict()
			jars = UserVariationQuantityHistorySerializer(UserVariationQuantityHistory.objects.filter(user=user), many=True)
			users = UserSerializer(user)
			if not user.nick_name:
				user.nick_name=""
			data = {
				# 'name':user.firstname + ' '+user.lastname +' ('+ user.nick_name +' )',
				# 'nick_name' : user.nick_name,
				# 'jars': jars.data,
				'users': users.data
			}
			import pprint
			pprint.pprint(data)
			#settings.dbgprint(data)
			return Response(data)
		else:
			return Response({"Fail":"Enter Phone number "}, status.HTTP_400_BAD_REQUEST)

class GetUserCreditAndJarByStorewise(APIView):
	def get_current_store(self):
		settings.DLFPRINT()
		store_id_auth_user = StoreUser.objects.filter(fk_user=self.request.user).first().fk_store
		# print(store_id_auth_user)
		credit_users_lists = StoreAccount.objects.filter(fk_store=store_id_auth_user)
		# print(credit_users_lists.__dict__)
		users_id=[]
		data = {'users': [],'credit':[], 'detail':[]}
		for user_id in credit_users_lists:
			# print(user_id.__dict__)
			users_id.append(user_id.fk_user_id)
			# data['users'].append(user_id.fk_user_id)
			# # data['credit'].append(user_id.credit)
			# abc=UserSerializer(User.objects.filter(pk=user_id.fk_user_id).first())
			# data['users':user_id.fk_user_id]['credit': user_id.credit] =[]
			# data.append(abc.data)
			
		# print(users_id)

		users_serializer = UserSerializer(User.objects.filter(pk__in=users_id), many=True)
		# data['detail'].append(users_serializer.data)
		response_data = {
			# 'data': data
			'count': len(users_id),
			'users': users_serializer.data
		}
		return Response(response_data)
		
	def get(self, request):
		settings.DLFPRINT()
		return self.get_current_store()



from orders.models import StoreWiseOrder
class GetCallLogsStoreAPIView(APIView):
	def post(self, request, *args, **kwargs):
		settings.DLFPRINT()
		# call_logs = [{'number': '9849298499', 'timestamp': '12891298128'}, {'number': '9849298499', 'timestamp': '12891298129'}]
		print(request.data)
		calls = request.data['calls']
		length = len(calls)
		if calls:
			for i in range(length):
				call = calls[i]
				#tmstmp_str = CallLog.objects.filter(is_existing=False);import pdb; pdb.set_trace(); ?? 
				db_calllog = CallLog.objects.filter(number=call.get('number')).filter(timestamp_str=call.get('timestamp')).first()
				if db_calllog: # save if call no and time are not  in db
					continue # already saved this number in db

				#all call logs are saved to db which are not saved already
				## saving new call log(timestamp + no) if it dont exit
				#make order if order is already preasent()
				#
				# maybe we need called number (kasko ma missed call ako)

				calllogs = CallLog()				
				cartitem_of_phone_q = CartItem.objects.filter(cart__user__mobile=call.get('number'))
				cartitem_of_phone = cartitem_of_phone_q.first()				
				
				if cartitem_of_phone: #if already order is preasent for that phone no
					#get variation with most orders
					variation_max = cartitem_of_phone_q.values('item_id') \
					.annotate(countgroup=Count('item_id')).order_by('-countgroup') \
					.first()
					
					calllogs.is_existing = True
					calllogs.fk_variation_id = variation_max.get('item_id')
					
					user_id = cartitem_of_phone.cart.user_id
					order = StoreWiseOrder.objects.filter(fk_auth_user_id=user_id) \
						.filter(~Q(order_latitude=None)).filter(~Q(order_longitude=None)) \
						.order_by('-id').first()
					calllogs.order_latitude = order.order_latitude
					calllogs.order_longitude = order.order_longitude

					
				calllogs.fk_staff_user = request.user
				calllogs.fk_store = getUserStoreService(request.user.id)
				calllogs.number = call.get('number')
				calllogs.timestamp_str = call.get('timestamp')
				calllogs.save()
			return Response('Success', status=200)
		return Response('failed to save', status=400)

from django.db.models import Q
# from store.service import getUserStoreService		
class MissCallUsersAPIView(APIView):
	def get(self, request):
		settings.DLFPRINT()
		users = User.objects.all()
		un_matched_users = CallLog.objects#.filter(is_existing=False)#.filter(~Q(number__in=users.values_list('mobile')))
		# print(un_matched_users)
		un_matched_users = un_matched_users.filter(staff_entry_at=None).filter(fk_store=getUserStoreService(request.user.id))
		data = CallLogSerializer(un_matched_users.all().order_by('timestamp') , many=True).data
		return Response(data)




# class CustomerPatientUserList(ListAPIView):
    # def get_context_data(self, **kwargs):
    #     ctx = super(CustomerPatientUserList, self).get_context_data(**kwargs)
    #     ctx['title'] = 'My Title'
    #     ctx['description'] = 'My Description'
    #     return ctx

from django.views.generic.list import ListView
from .serializer import DoctorSerializer, VisitSeriailizer
from .models import Doctor
class CustomerPatientUserList(ListView):
	model = Account
	template_name = "personal/dashboard_layout/patients.html"
	paginate_by = 20

	def get_queryset(self):
		q = self.request.GET.get('q')
		new_context = Account.objects.all()
		return new_context

	def get_context_data(self, **kwargs):
		context = super(CustomerPatientUserList, self).get_context_data(**kwargs)
		context['patient_types'] = UserTypes.objects.all()
		# context['filter'] = self.request.GET.get('filter', 'give-default-value')
		# context['orderby'] = self.request.GET.get('orderby', 'give-default-value')

		return context

class PatientUserListAPIView(APIView):
	serializer_class = PatientSerializer
	class Meta:
		model = User
	def get(self, request):
		pids = UserType.objects.all()
		patients = User.objects.filter(pk__in=pids.values('user_id'))
		return Response(PatientSerializer(patients, many=True).data)

		
class DoctorUserListAPIView(ListAPIView):
	serializer_class = DoctorSerializer

	def get_queryset(self):
		doctors_assigned = Doctor.objects.all()
		queryset = User.objects.filter(id__in=doctors_assigned.values('fk_user_id'))
		return queryset

# class VisitListAPIView(ListView):
	
# 	def get_queryset(self):
# 		doctors_assigned = Doctor.objects.all()
# 		queryset = User.objects.filter(id__in=doctors_assigned.values('fk_user_id'))
# 		return queryset



class VisitAPIView(APIView):
	serializer_class = VisitSeriailizer

	def get(self, request):
		visit_types = VisitType.objects.all()
		customer_id = request.GET.get('customer_id')
		customer_mobile = request.GET.get('customer_mobile')
		customer_name = request.GET.get('customer_name')
		visit_date = request.GET.get('visit_date')
		#dt.datetime(strptime(visit_date, '%Y-%m-%d'))
		fk_visit = request.GET.get('fk_visit')
		qs = Visit.objects
		if customer_id:
			qs = qs.filter(fk_customer_user_id=customer_id)
		if customer_mobile:
			qs = qs.filter(fk_customer_user__mobile=customer_mobile)
		if customer_name:
			qs=qs.filter(fk_customer_user__firstname=customer_name, fk_customer_user__lastname=customer_name)
		if visit_date:
			visit_datetime_obj = dt.fromisoformat(visit_date)
			qs = qs.filter(timestamp__gte=visit_datetime_obj, timestamp__lte=visit_datetime_obj+timedelta(hours=23, minutes=59, seconds=29))#all()
		if fk_visit:
			qs = qs.filter(fk_visit__id=fk_visit)
		else:
			qs = qs.filter(timestamp__gte=timezone.now().replace(hour=0, minute=0, second=0), timestamp__lte=timezone.now().replace(hour=23, minute=59, second=59))#all()
		paginator = Paginator(qs, 5)  # Show 25 contacts per page
		# Get the current page number
		page = request.GET.get('page')
		# Get the current slice (page) of products
		qs = paginator.get_page(page)
		template_name = "personal/dashboard_layout/visits.html"
		return render(request, template_name, {'visits': qs, 'visit_types': visit_types})

	
		
	def post(self, request):
		print(request.data)
		fk_customer_user_id = request.data.get('fk_customer_user_id')
		fk_doctor_user_id =  request.data.get('fk_doctor_user_id')
		remarks =  request.data.get('remarks')
		appointment_date =  request.data.get('appointmentDate')
		fk_bloodgroup_id = request.data.get('fk_bloodgroup_id')
		emergency_number = request.data.get('emergency_number')	
		if fk_customer_user_id and fk_doctor_user_id:
			visit = Visit.objects.create(fk_customer_user_id=fk_customer_user_id,
										 fk_doctor_user_id=fk_doctor_user_id,
										 appointment_date=appointment_date,
										 fk_visit_id=visit_type,
										 fk_blood_id=fk_bloodgroup_id,
										 emergency_number = emergency_number,
										 remarks=remarks)
			data = {
				'success': 'Created',
				'id' : visit.id,
				'fk_customer_user_id' :visit.fk_customer_user_id
			}
			return Response(data, status=200)
		else:
			return Response('failed', status=400)



# Create your views here.
def visit_type_index(request):
	visit_types = VisitType.objects.all()
	return render(request, 'account/visit_type_index.html', {'visit_types': visit_types})

from .forms import VisitTypeForm
def  visit_type_add(request):
	fstatusType = "Add"
	fpostType = "Visit Type"

	if request.method=='POST':
		visit_types = VisitTypeForm(request.POST)

		if visit_types.is_valid():
			print('Passed')
			visit_types.save()
			return redirect('/visit-type/', messages.success(request, 'Visit Type added successfully.', 'alert-success'))
			# return HttpResponse('Added successfully')
		else:
			print(vendor_details.errors)
			print('Failed')
			return redirect('/visit-type/', messages.success(request, 'All fields are required.', 'alert-success'))
	else:
		form = VisitTypeForm()
	
	return render(request, 'account/visit_type_add.html', {'form':form, 'fstatusType': fstatusType, 'fpostType': fpostType})




def visit_type_edit(request, id):
	visit_types = VisitTypeForm(request.POST)

	fstatusType = "Update"
	fpostType = "Visit Type"
	if request.method=='POST':
		form = VisitTypeForm(request.POST, instance=visit_types)

		if form.is_valid():
			print('Passed')
			if form.save():
				# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Education Info added successfully.', 'alert-success'))
				return redirect('/visit-type/', messages.success(request, 'Vendor Management updated successfully', 'alert-success'))
			else:
				return redirect('/visit-type/', messages.success(request, 'There was a problem connecting to the server. Please try again later.', 'alert-success'))
			form.save()
			# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Educations Info added successfully.', 'alert-success'))
	else:
		form = VisitTypeForm(instance=visit_types)

	return render(request, 'account/visit_type_add.html', {'form':form, 'fpostType':fpostType})


def delete(request, id):
	print(id)


