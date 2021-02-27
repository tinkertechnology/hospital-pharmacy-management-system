
from orders.utils import render_to_pdf, render_to_pdf_value
from rest_framework.views import APIView
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from orders.models import *
from carts.models import *
from .convert_num_to_words import generate_amount_words

class GeneratePDF(APIView):
	def get(self, request, cart_id, *args, **kwargs):
		something = request.GET.get('preview', None)
		cart_id = cart_id
		# print(kwargs)
        # print(cart_id)
		if not cart_id: #fk_storewise_order_id passed here
			return HttpResponse('no order id')
		# order = StoreWiseOrder.objects.filter(order_id=order_id).first()
		# ordered_cart_id = order.cart_id
		cart = Cart.objects.filter(pk=cart_id).first()
		# print(order)
		total_in_words = generate_amount_words(cart.total)
		print(total_in_words)
		items = cart.cartitem_set.all()#CartItem.objects.filter(cart_id=ordered_cart_id)
		# print(items);

		# print(order)
		# cart_items = CartItem.objects.filter(fk_storewise_order_id=order_id) WIll be relevant when multple pharmacy stores are present
		# cart_items = 

		# print(cart_items)



		# print(id)
		# queryset = Quote.objects.filter(id=id).first()
		# customer = queryset.fk_customer
		# quote = Quote.objects.get(id=id)
		# quote_items = QuoteItem.objects.filter(fk_quote=id)
		# subtotal = calculate_quote_price(quote_items)
		# int_subtotal = int(subtotal)
		# discount_amount = 0
		# print(int_subtotal)
		# if(quote.quote_discount_percent):
		# 	discount_amount = round(quote.quote_discount_percent * 0.01 * int_subtotal, 2)
		# print(discount_amount) 
		# taxable_amount = int_subtotal - discount_amount
		# vat_amount = 0.13*taxable_amount
		# int_vatAmount = round(vat_amount, 2)
		# print(int_vatAmount)
		# total_price = taxable_amount+int_vatAmount
		# int_totalPrice = round(total_price, 2) 
		# quoted_by = User.objects.get(id=quote.created_by_id)
		# print(quoted_by)
		# # print(item.fk_customer.name)
		# try:
		# 	site_info = Site.objects.get(id=1)

		# except ObjectDoesNotExist:
		# 	site_info = {
	 #        'title': 'Test Company',
	 #        'email': 'test@test.com',
	 #        'address': 'address',
	 #        'vat_no': 'vat_no',
	 #        'phone_no': 'phone_no'
	 #        }

		# print(queryset)
		template = get_template('personal/dashboard_layout/invoice.html')
		context = {

			'cart': cart,
			'items': items,
			'total_in_words':total_in_words

			# 'item': queryset,
			# 'item': quote,
			# 'quote_items' : quote_items,
			# 'subtotal': subtotal,
			# 'discount_amount' : discount_amount,
			# 'taxable_amount' : taxable_amount,
			# 'vat_amount' : int_vatAmount,
			# 'total_price': int_totalPrice,
			# 'quoted_by': quoted_by,
			# 'site_info': site_info,

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