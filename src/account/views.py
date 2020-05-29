from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response


from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from blog.models import BlogPost
from .models import Account, PhoneOTP
from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404 
import random
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
			print(mobile)
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
						old.save()
						print('increaded count', count)

						return Response({
							'status': True,
							'detail' : 'OTP sent sucessfully'

							})

					else:

						PhoneOTP.objects.create(
							mobile = mobile,
							otp = key,

							)
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
		return key
	else :
		return False











