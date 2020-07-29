from decimal import Decimal
from django.conf import settings
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
# Create your models here.
from carts.models import Cart
from products.models import Product

from payment.models import PaymentMethod
from store.models import Store
from routes.models import Route
from django.contrib.auth import get_user_model
User = get_user_model()

import braintree

if settings.DEBUG:
	braintree.Configuration.configure(braintree.Environment.Sandbox,
      merchant_id=settings.BRAINTREE_MERCHANT_ID,
      public_key=settings.BRAINTREE_PUBLIC,
      private_key=settings.BRAINTREE_PRIVATE)



class UserCheckout(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) #not required
	email = models.EmailField(unique=True) #--> required
	braintree_id = models.CharField(max_length=120, null=True, blank=True)

	def __str__(self): #def __str__(self):
		return self.email

	@property
	def get_braintree_id(self,):
		instance = self
		if not instance.braintree_id:
			result = braintree.Customer.create({
			    "email": instance.email,
			})
			if result.is_success:
				instance.braintree_id = result.customer.id
				instance.save()
		return instance.braintree_id

	def get_client_token(self):
		customer_id = self.get_braintree_id
		if customer_id:
			client_token = braintree.ClientToken.generate({
			    "customer_id": customer_id
			})
			return client_token
		return None


def update_braintree_id(sender, instance, *args, **kwargs):
	if not instance.braintree_id:
		instance.get_braintree_id


post_save.connect(update_braintree_id, sender=UserCheckout)




ADDRESS_TYPE = (
	('billing', 'Billing'),
	('shipping', 'Shipping'),
)

class UserAddress(models.Model):
	user = models.ForeignKey(UserCheckout, on_delete=models.CASCADE, blank=True)
	type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
	street = models.CharField(max_length=120)
	city = models.CharField(max_length=120)
	state = models.CharField(max_length=120)
	zipcode = models.CharField(max_length=120)
	phone = models.CharField(max_length=120, null=True)

	def __str__(self):
		return self.street

	def get_address(self):
		return "%s, %s, %s %s" %(self.street, self.city, self.state, self.zipcode)


ORDER_STATUS_CHOICES = (
	('created', 'Created'),
	('paid', 'Paid'),
	('shipped', 'Shipped'),
	('refunded', 'Refunded'),
)


class Order(models.Model):
	status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	user = models.ForeignKey(UserCheckout,on_delete=models.CASCADE, null=True, )
	billing_address = models.ForeignKey(UserAddress,on_delete=models.CASCADE, related_name='billing_address', blank=True, null=True)
	shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='shipping_address', blank=True, null=True)
	shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99)
	order_total = models.DecimalField(max_digits=50, decimal_places=2, )
	tax_amount = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	
	grand_total_amount = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	order_id = models.CharField(max_length=20, null=True, blank=True)
	fk_auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	is_delivered = models.BooleanField(default=False)
	fk_ordered_store = models.ForeignKey(Store, related_name='fk_ordered_store', on_delete=models.CASCADE, null=True, blank=True)
	fk_delivery_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fk_delivery_user', on_delete=models.CASCADE, null=True, blank=True)
	is_paid = models.BooleanField(default=False)
	fk_payment_method = models.ForeignKey(PaymentMethod, related_name='fk_ordered_store', on_delete=models.CASCADE, null=True, blank=True)
	fk_ordered_by_store = models.ForeignKey(Store, related_name='fk_ordered_by_store', on_delete=models.CASCADE, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	order_latitude = models.CharField(max_length=200, null=True, blank=True)
	order_longitude = models.CharField(max_length=200, null=True, blank=True)
	is_auto_order = models.BooleanField(default=False)


	def __str__(self):
		return "Order_id: %s, Cart_id: %s"%(self.id, self.cart.id)

	class Meta:
		ordering = ['-id']

	def get_absolute_url(self):
		return reverse("order_detail", kwargs={"pk": self.pk})

	def mark_completed(self, order_id=None):
		self.status = "paid"
		if order_id and not self.order_id:
			self.order_id = order_id
		self.save()

	@property
	def is_complete(self):
		if self.status == "paid":
			return True
		return False


def order_pre_save(sender, instance, *args, **kwargs):
	print('noobs')
	shipping_total_price = instance.shipping_total_price
	cart_total = instance.cart.total
	order_total = Decimal(shipping_total_price) + Decimal(cart_total)
	instance.order_total = order_total

pre_save.connect(order_pre_save, sender=Order)

# #if status == "refunded":
# 	braintree refud
# post_save.connect()

# 	

class StoreWiseOrder(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99)
	order_total = models.DecimalField(max_digits=50, decimal_places=2, )
	tax_amount = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	grand_total_amount = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	order_id = models.CharField(max_length=20, null=True, blank=True)
	fk_auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	is_delivered = models.BooleanField(default=False)
	fk_ordered_store = models.ForeignKey(Store, related_name='fk_ordered_store_storewiseorder', on_delete=models.CASCADE, null=True, blank=True)
	fk_delivery_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fk_delivery_user_storewiseorder', on_delete=models.CASCADE, null=True, blank=True)
	is_paid = models.BooleanField(default=False)
	is_transit = models.BooleanField(default=False)
	fk_payment_method = models.ForeignKey(PaymentMethod, related_name='fk_ordered_store_storewiseorder', on_delete=models.CASCADE, null=True, blank=True)
	fk_ordered_by_store = models.ForeignKey(Store, related_name='fk_ordered_by_store_storewiseorder', on_delete=models.CASCADE, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	order_latitude = models.CharField(max_length=200, null=True, blank=True)
	order_longitude = models.CharField(max_length=200, null=True, blank=True)
	fk_route = models.ForeignKey(Route, related_name='fk_route_storewiseorder', on_delete=models.CASCADE, null=True, blank=True)
	is_auto_order = models.BooleanField(default=False)
	
	class Meta:
		ordering = ['-created_at']



class Quotation(models.Model):
	fk_product = models.ForeignKey(Product, on_delete=models.CASCADE)
	email = models.CharField(max_length=200, null=True, blank=True)
	message = models.CharField(max_length=200,null=True,blank=True)

	class Meta:
		ordering = ['-id']
	def __str__(self):
		return '%s %s' %(self.email, self.message) 





