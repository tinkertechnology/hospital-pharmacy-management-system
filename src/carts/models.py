from decimal import Decimal
from django.conf import settings
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth import get_user_model
User = get_user_model()
# from orders.models import StoreWiseOrder



from products.models import Variation
# Create your models here.


class CartItem(models.Model):
	cart = models.ForeignKey("Cart", on_delete=models.CASCADE, blank=True)

	# will be filled later
	# after this cart item is added to storewiseorder table
	# fk_storewise_order = models.ForeignKey("orders.StoreWiseOrder", on_delete=models.CASCADE, blank=True, null=True) 
	item = models.ForeignKey(Variation, on_delete=models.CASCADE)
	# quantity = models.PositiveIntegerField(default=1)
	quantity = models.DecimalField(max_digits=25, decimal_places=2, default=1.00)	
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
	if Decimal(qty) >= 0:
		price = instance.item.get_price()
		if instance.ordered_price!=0:
			price = instance.ordered_price
		instance.orginal_price = price
		# if qty>=3:
		# 	price = price-Decimal(float(price)*(3/10))
		# elif qty>=2:
		# 	price = price-Decimal(float(price)*(2/10))
		instance.ordered_price = price
		line_item_total = Decimal(qty) * Decimal(price)
		instance.line_item_total = line_item_total
		instance.tax_amount = Decimal(float(line_item_total)*settings.TAX_PERCENT_DECIMAL)

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)



def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
	instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	items = models.ManyToManyField(Variation, through=CartItem)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	tax_percentage  = models.DecimalField(max_digits=10, decimal_places=5, default=0.085)
	tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	#user ko cart active 1uta matrai huncha db ma...
	#create_order garepachi 0 set huncha... yo bhaneko user ko cart chaina 
	#1 bhayo bhane usko cart ma aru item ne add huncha. 
	active = models.BooleanField(default=True)
	fk_bill_created_user = models.ForeignKey(User, related_name="bill_created_by", on_delete=models.CASCADE, null=True, blank=True)
	# 0 online order , 1 offline staff order , 2 misscall order 
	is_auto_order = models.IntegerField(default=0) 
	credit = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, null=True, blank=True)
	debit = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, null=True, blank=True)
	fk_delivery_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="delivery_user", on_delete=models.CASCADE, null=True, blank=True, default=None) 
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
	instance.tax_total =  "%.2f" %(tax_total)
	instance.total = "%.2f" %(total)
	# instance.save()



pre_save.connect(do_tax_and_total_receiver, sender=Cart)




class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
	comment = models.CharField(max_length=500, null=True, blank=True)
	created_at =  models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at =  models.DateTimeField(auto_now_add=True, auto_now=False)
	def __unicode__(self):
		return self.user.mobile


class TransactionType(models.Model):
	title = models.CharField(max_length=100, null=True, blank=True)
	def __str__(self):
		return self.title

class Transaction(models.Model):
	date = models.DateTimeField(auto_now_add=True, auto_now=False)
	fk_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, null=True)
	amount = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
	comment = models.CharField(null=True, max_length=100, blank=True)
	entered_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	fk_cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		return '%s %s' %(self.amount, self.fk_type.title)






