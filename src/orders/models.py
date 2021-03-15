from decimal import Decimal
from django.conf import settings
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
# Create your models here.
from carts.models import Cart
from products.models import Product, Variation, VariationBatch

from payment.models import PaymentMethod
from store.models import Store
from django.contrib.auth import get_user_model
User = get_user_model()
from vendor.models import Vendor

# import braintree

# if settings.DEBUG:
# 	braintree.Configuration.configure(braintree.Environment.Sandbox,
#       merchant_id=settings.BRAINTREE_MERCHANT_ID,
#       public_key=settings.BRAINTREE_PUBLIC,
#       private_key=settings.BRAINTREE_PRIVATE)



ORDER_STATUS_CHOICES = (
	('created', 'Created'),
	('paid', 'Paid'),
	('shipped', 'Shipped'),
	('refunded', 'Refunded'),
)


class Order(models.Model):
	status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	# user = models.ForeignKey(UserCheckout,on_delete=models.CASCADE, null=True, )
	# billing_address = models.ForeignKey(UserAddress,on_delete=models.CASCADE, related_name='billing_address', blank=True, null=True)
	# shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='shipping_address', blank=True, null=True)
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
	is_auto_order = models.IntegerField(default=0)


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
	remarks = models.CharField(max_length=500, null=True, blank=True)
	is_cancelled = models.BooleanField(default=False)
	cancelled_at = models.DateTimeField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	order_latitude = models.CharField(max_length=200, null=True, blank=True)
	order_longitude = models.CharField(max_length=200, null=True, blank=True)
	is_auto_order = models.IntegerField(default=0)
	
	class Meta:
		ordering = ['-id']

from products.models import ProductUnit
class PurchaseItem(models.Model):
	fk_purchase = models.ForeignKey("Purchase", related_name="purchaseitems", on_delete=models.CASCADE, blank=True)
	fk_variation = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True)
	# quantity = models.PositiveIntegerField(default=1)
	quantity = models.DecimalField(max_digits=25, decimal_places=2, default=1.00)	
	tax_amount = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	line_item_total = models.DecimalField(max_digits=10, default=0.00, decimal_places=2, blank=True)
	orginal_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	ordered_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	batchno = models.CharField(null=True, blank=True, max_length=100)
	free_quantity = models.DecimalField(max_digits=25, decimal_places=2, default=1.00)	
	total_quantity = models.DecimalField(max_digits=25, decimal_places=2, default=1.00)	
	cost_price = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
	sell_price = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
	is_return = models.BooleanField(default=False, null=True, blank=True)
	fk_product_unit =  models.ForeignKey(ProductUnit, on_delete=models.CASCADE, null=True, blank=True)
	packaging_quantity  = models.DecimalField(max_digits=25, decimal_places=2, default=1.00)	
	expiry_date = models.DateField(null=True, blank=True)


	def __unicode__(self):
		return self.fk_variation.title


def purchase_item_post_save_receiver(sender, instance, *args, **kwargs):
	instance.fk_purchase.update_subtotal()
post_save.connect(purchase_item_post_save_receiver, sender=PurchaseItem)


class Purchase(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	# purchaseitems = models.ManyToManyField(PurchaseItem, related_name="purchaseitems")
	bill_date = models.DateField(null=True, blank=True)
	purchase_date = models.DateField(null=True, blank=True)
	fk_vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)

	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	tax_percentage  = models.DecimalField(max_digits=10, decimal_places=5, default=0.085)
	tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	active = models.BooleanField(default=True)
	credit = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, null=True, blank=True)
	debit = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, null=True, blank=True)
	grand_total = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, null=True, blank=True)
	fk_payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.CASCADE, blank=True)
	

	def __unicode__(self):
		return str(self.id)

	def update_subtotal(self):
		print("updating...")
		subtotal = 0
		items = self.purchaseitems.all()
		for item in items:
			subtotal += item.line_item_total
		self.subtotal = "%.2f" %(subtotal)
		self.save()



