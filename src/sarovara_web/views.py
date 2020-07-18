from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib import messages
from io import BytesIO
import mimetypes
import smtplib

from .forms import * 

def index(request):
	page_title = 'Home'
	return render(request, 'sarovara/index.html', {'title_content':page_title})
	# return HttpResponse('index page')


def we_sales(request):
	page_title = 'We sales'
	return render(request, 'sarovara/sales.html', {'title_content':page_title})


def our_depot(request):
	page_title = 'Our Depot'
	return render(request, 'sarovara/depot.html', {'title_content':page_title})

def about_us(request):
	page_title = 'About Us'
	return render(request, 'sarovara/about_us.html', {'title_content':page_title})

def contacts(request):
	page_title = 'Contact Us'
	return render(request, 'sarovara/contacts.html', {'title_content':page_title})

def terms_of_use(request):
	page_title = 'Terms of Use'
	return render(request, 'sarovara/terms_of_use.html', {'title_content':page_title})

def buy_drinking_water(request):
	page_title = 'Buy Drinking Water'
	return render(request, 'sarovara/buy-drinking-water.html', {'title_content':page_title})

def sell_drinking_water(request):
	page_title = 'Sell Drinking Water'
	return render(request, 'sarovara/sell-drinking-water.html', {'title_content':page_title})

def open_depot(request):
	page_title = 'Open Depot'
	return render(request, 'sarovara/open-depot.html', {'title_content':page_title})

def feedback(request):
	page_title = 'Provide Feedback'
	return render(request, 'sarovara/feedback.html', {'title_content':page_title})

def complaint(request):
	page_title = 'Complaint or Grievance'
	return render(request, 'sarovara/complaint.html', {'title_content':page_title})

def careers(request):
	page_title = 'Careers'
	return render(request, 'sarovara/careers.html', {'title_content':page_title})


def vacancy_apply_now(request):
	page_title = 'Apply Now'
	return render(request, 'sarovara/vacancy_apply_now.html', {'title_content':page_title})


def buy_drinking_water(request):
	if request.method == 'GET':
		form = BuyDrinkingWaterForm()
		# print (form)
	else:
		print (1234)
		success = False
		form = BuyDrinkingWaterForm(request.POST)
		print(form.errors)
		if form.is_valid():
			print(12345)
			select_location = form.cleaned_data['select_location']
			full_name = form.cleaned_data['full_name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			select_depot = form.cleaned_data['select_depot']
			select_brand = form.cleaned_data['select_brand']
			select_purchase_type = form.cleaned_data['select_purchase_type']
			
			# message_body = form.cleaned_data['message']
			message = (
                'Dear Sarovara, \nYou have received mail from '+ full_name + ', ' + select_location + ' for ' + select_brand + '\n' 
	                + 'Phone: ' + phone + '\n' 
	                + 'Email: ' + email + '\n'
	                + 'Purchase Type: ' + select_purchase_type
                )
			from_email = email
			to_email = ['asndesh28@gmail.com', settings.EMAIL_HOST_USER]
			subject = 'Buy Drinking Water from Sarovara'
			try:
				print(123456)
				# to_list = ['info@wonderwheels.com.np', settings.EMAIL_HOST_USER]
				messages.success(request, 'Your message has been successfully!')
				send_mail(subject, message, from_email, to_email, fail_silently=False)
				# return JsonResponse('Success', safe=False)
				return HttpResponseRedirect('buy-drinking-water')
			except BadHeaderError:
				print(1234567)
				return HttpResponse('Invalid header found.')
			# return redirect('success')
		else:
			messages.warning(request, 'Error occured. Please try again later.')
	return render(request, 'sarovara/buy-drinking-water.html', {'form': form})


def request_open_depot(request):
	if request.method == 'GET':
		form = OpenDepotForm()
		# print (form)
	else:
		print (1234)
		success = False
		form = OpenDepotForm(request.POST)
		print(form.errors)
		if form.is_valid():
			print(12345)
			location = form.cleaned_data['location']
			full_name = form.cleaned_data['full_name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			message_body = form.cleaned_data['message']
			message = (
                'Dear Sarovara, \nYou have received mail from '+ full_name + ', ' + location + '.' +  '\n' 
	                + 'Phone: ' + phone + '\n' 
	                + 'Email: ' + email + '\n'
	                + 'Message: ' + message_body
                )
			from_email = email
			to_email = ['asndesh28@gmail.com', settings.EMAIL_HOST_USER]
			subject = 'Request for Depot'
			try:
				print(123456)
				# to_list = ['info@wonderwheels.com.np', settings.EMAIL_HOST_USER]
				messages.success(request, 'Your message has been successfully!')
				send_mail(subject, message, from_email, to_email, fail_silently=False)
				# return JsonResponse('Success', safe=False)
				return HttpResponseRedirect('open-depot')
			except BadHeaderError:
				print(1234567)
				return HttpResponse('Invalid header found.')
			# return redirect('success')
		else:
			messages.warning(request, 'Error occured. Please try again later.')
	return render(request, 'sarovara/open-depot.html', {'form': form})


def request_feedback(request):
	if request.method == 'GET':
		form = FeedbackForm()
		# print (form)
	else:
		print (1234)
		success = False
		form = FeedbackForm(request.POST)
		print(form.errors)
		if form.is_valid():
			print(12345)
			full_name = form.cleaned_data['full_name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			message_body = form.cleaned_data['message']
			message = (
                'Dear Sarovara, \nYou have received mail from '+ full_name + ' for feedback. ' +  '\n' 
	                + 'Phone: ' + phone + '\n' 
	                + 'Email: ' + email + '\n'
	                + 'Message: ' + message_body
                )
			from_email = email
			to_email = ['asndesh28@gmail.com', settings.EMAIL_HOST_USER]
			subject = 'Request for Feedback'
			try:
				print(123456)
				# to_list = ['info@wonderwheels.com.np', settings.EMAIL_HOST_USER]
				messages.success(request, 'Your message has been successfully!')
				send_mail(subject, message, from_email, to_email, fail_silently=False)
				# return JsonResponse('Success', safe=False)
				return HttpResponseRedirect('feedback')
			except BadHeaderError:
				print(1234567)
				return HttpResponse('Invalid header found.')
			# return redirect('success')
		else:
			messages.warning(request, 'Error occured. Please try again later.')
	return render(request, 'sarovara/feedback.html', {'form': form})


def request_complaint(request):
	if request.method == 'GET':
		form = ComplaintForm()
		# print (form)
	else:
		print (1234)
		success = False
		form = ComplaintForm(request.POST)
		print(form.errors)
		if form.is_valid():
			print(12345)
			select_location = form.cleaned_data['select_location']
			full_name = form.cleaned_data['full_name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			message_body = form.cleaned_data['message']
			message = (
                'Dear Sarovara, \nYou have received mail from '+ full_name + ' for complaint request for ' + select_location + '.' +  '\n' 
	                + 'Phone: ' + phone + '\n' 
	                + 'Email: ' + email + '\n'
	                + 'Message: ' + message_body
                )
			from_email = email
			to_email = ['asndesh28@gmail.com', settings.EMAIL_HOST_USER]
			subject = 'Request for Complaint'
			try:
				print(123456)
				# to_list = ['info@wonderwheels.com.np', settings.EMAIL_HOST_USER]
				messages.success(request, 'Your message has been successfully!')
				send_mail(subject, message, from_email, to_email, fail_silently=False)
				# return JsonResponse('Success', safe=False)
				return HttpResponseRedirect('complaint')
			except BadHeaderError:
				print(1234567)
				return HttpResponse('Invalid header found.')
			# return redirect('success')
		else:
			messages.warning(request, 'Error occured. Please try again later.')
	return render(request, 'sarovara/complaint.html', {'form': form})


def apply_vacancy_now(request):
	if request.method == 'POST':
		print (1234)
		# success = False
		form = VacancyForm(request.POST, request.FILES)
		print(form.errors)
		# print(VacancyForm())
		if form.is_valid():
			print(12345)
			full_name = form.cleaned_data['full_name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			address = form.cleaned_data['address']
			cv = request.FILES['cv']
			citizenship = request.FILES['citizenship']
			# message_body = form.cleaned_data['message']
			message = (
                'Dear Sarovara, \nYou have received mail from '+ full_name + '\n' 
	                + 'Phone: ' + phone + '\n' 
	                + 'Email: ' + email + '\n'
	                + 'Address: ' + address + '\n'
	                # + 'Curriculum Vitae: ' + cv + '\n'
	                # + 'Citizenship: ' + citizenship + '\n'
                )
			from_email = email
			to_email = ['asndesh28@gmail.com', settings.EMAIL_HOST_USER]
			subject = 'Request for Vacancy'
			try:
				print(123456)
				# to_list = ['info@wonderwheels.com.np', settings.EMAIL_HOST_USER]
				# messages.success(request, 'Your message has been successfully!')
				mail = EmailMessage(subject, message, from_email, to_email)
				mail.attach(cv.name, cv.read(), cv.content_type)
				mail.attach(citizenship.name, citizenship.read(), citizenship.content_type)
				mail.send()
				# return JsonResponse('Success', safe=False)
				# return HttpResponseRedirect('apply-vacancy-now')
				return render(request, 'sarovara/vacancy_apply_now.html', {'form': form, 'error_message':'Mail sent successfully !!!'})
			except BadHeaderError:
				print(1234567)
				return HttpResponse('Invalid header found.')
			# return redirect('success')
		else:
			messages.warning(request, 'Error occured. Please try again later.')
	return render(request, 'sarovara/vacancy_apply_now.html', {'form': form})

# def success(request):
# 	return HttpResponse('Success! Thank you for your email.')