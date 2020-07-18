from decimal import Decimal
from django.conf import settings
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
# from orders.models import StoreWiseOrder



from products.models import Variation
# Create your models here.


class CartItem(models.Model):
	cart = models.ForeignKey("Cart", on_delete=models.CASCADE, blank=True)

	# will be filled later
	# after this cart item is added to storewiseorder table
	fk_storewise_order = models.ForeignKey("orders.StoreWiseOrder", on_delete=models.CASCADE, blank=True, null=True) 
	item = models.ForeignKey(Variation, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	tax_amount = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	line_item_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
	orginal_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	ordered_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)	

	def __unicode__(self):
		return self.item.title

	def remove(self):
		return self.item.remove_from_cart()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
	qty = instance.quantity
	if Decimal(qty) >= 1:
		price = instance.item.get_price()
		if instance.fk_storewise_order is not None:	
			pass	# price = instance.ordered_price
		else:
			instance.orginal_price = price
			if qty>=3:
				price = price-Decimal(float(price)*(3/10))
			elif qty>=2:
				price = price-Decimal(float(price)*(2/10))

			instance.ordered_price = price

			line_item_total = Decimal(qty) * Decimal(price)
			instance.line_item_total = line_item_total
			instance.tax_amount = Decimal(float(line_item_total)*0.13)


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)



def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
	instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	items = models.ManyToManyField(Variation, through=CartItem)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	tax_percentage  = models.DecimalField(max_digits=10, decimal_places=5, default=0.085)
	tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	active = models.BooleanField(default=True)
	# fk_status

	# discounts
	# shipping

	def __unicode__(self):
		return str(self.id)

	def update_subtotal(self):
		print("updating...")
		subtotal = 0
		items = self.cartitem_set.all()
		for item in items:
			subtotal += item.line_item_total
		self.subtotal = "%.2f" %(subtotal)
		self.save()

	def is_complete(self):
		self.active = False
		self.save()




def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
	subtotal = Decimal(instance.subtotal)
	tax_total = round(subtotal * Decimal(instance.tax_percentage), 2) #8.5%
	print(instance.tax_percentage)
	total = round(subtotal + Decimal(tax_total), 2)
	instance.tax_total = "%.2f" %(tax_total)
	instance.total = "%.2f" %(total)
	#instance.save()



pre_save.connect(do_tax_and_total_receiver, sender=Cart)









