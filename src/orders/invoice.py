
from orders.utils import render_to_pdf, render_to_pdf_value
from rest_framework.views import APIView
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from orders.models import *
from carts.models import Cart
from office.models import Office
from .convert_num_to_words import generate_amount_words

class GeneratePDF(APIView):
	def get(self, request, cart_id, *args, **kwargs):
		something = request.GET.get('preview', None)
		hospital_info = Office.objects.all().first()
		cart_id = cart_id
		if not cart_id: #fk_storewise_order_id passed here
			return HttpResponse('no order id')
		cart = Cart.objects.filter(pk=cart_id).first()
		total_in_words = generate_amount_words(cart.total)
		print(total_in_words)
		items = cart.cartitem_set.all()#CartItem.objects.filter(cart_id=ordered_cart_id)
		template = get_template('personal/dashboard_layout/invoice.html')
		context = {
			'cart': cart,
			'items': items,
			'total_in_words':total_in_words,
			'hospital_info' : hospital_info
		}

		mail = EmailMessage(
		    'Hello', #+ customer.name,
		    'Quotation from Tinker-Tech',
		    'xunilparajuli2002@gmail.com',
		    #[customer.email],
		    ['sunilparajuli2002@gmail.com'],
		    reply_to=['sunilparajuli2002@gmail.com'],
		    headers={'Message-ID': 'foo'},
		)

		html = template.render(context)
		pdf_value = render_to_pdf_value('orders/invoice.html', context)
		pdf = render_to_pdf('orders/invoice.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Invoice_%s.pdf" %("12341231")
			if(something !='1'):
				print('email attach')
				mail.attach(filename, pdf_value, 'application/pdf')
				# mail.send()
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename=%s" %(filename)
				response['Content-Disposition'] = content
			return response
			return HttpResponse("Not found")
		# return HttpResponse(pdf, content_type='application/pdf')

class GenerateFullPDF(APIView):
	def get(self, request, cart_id, *args, **kwargs):
		something = request.GET.get('preview', None)
		hospital_info = Office.objects.all().first()	
		user_id = request.GET.get('user_id')
		# print(user_id)
		carts = Cart.objects.filter(user_id=user_id).order_by('-timestamp')
		total_sum_amount = sum(carts.values_list('total', flat=True))
		total_sum_subtotal = sum(carts.values_list('subtotal', flat=True))
		# print(dict_total)
		# total_sum_of_all_carts = sum(items.values_list('price', flat=True))
		
		total_in_words = generate_amount_words(total_sum_amount)
		printed_by = request.user.firstname +' '+ request.user.lastname
		print(total_in_words)
		# items = cart.cartitem_set.all()#CartItem.objects.filter(cart_id=ordered_cart_id)
		template = get_template('personal/dashboard_layout/invoice_full.html')
		context = {
			'carts': carts,
			# 'items': items,
			'total_in_words':total_in_words,
			'hospital_info' : hospital_info,
			'total_sum_subtotal' : total_sum_subtotal,
			'total_sum_amount':total_sum_amount,
			'printed_by' : printed_by

		}

		mail = EmailMessage(
		    'Hello', #+ customer.name,
		    'Quotation from Tinker-Tech',
		    'xunilparajuli2002@gmail.com',
		    #[customer.email],
		    ['sunilparajuli2002@gmail.com'],
		    reply_to=['sunilparajuli2002@gmail.com'],
		    headers={'Message-ID': 'foo'},
		)

		html = template.render(context)
		pdf_value = render_to_pdf_value('orders/invoice_full.html', context)
		pdf = render_to_pdf('orders/invoice_full.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Invoice_%s.pdf" %("12341231")
			if(something !='1'):
				print('email attach')
				mail.attach(filename, pdf_value, 'application/pdf')
				# mail.send()
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename=%s" %(filename)
				response['Content-Disposition'] = content
			return response
			return HttpResponse("Not found")
		# return HttpResponse(pdf, content_type='application/pdf')