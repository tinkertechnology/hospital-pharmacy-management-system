from django.db import models
from django.conf import settings

# Create your models here.

# class Inquiry(models.Model):

# 	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
# 	date = models.DateTimeField(auto_now_add=True, blank=True)
# 	description = models.TextField(blank=True, null=True)

# 	def __str__(self):
# 		return  'INQUIRY  BY USER- %s'  %(self.user.username)

# class Inquiry(models.Model):
# 	# user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
# 	# items = models.ManyToManyField(InquiryChat)
# 	send_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="send_from", on_delete=models.CASCADE, null=True, blank=True)
# 	send_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="send_to", on_delete=models.CASCADE, null=True, blank=True)
# 	timestamp = models.DateTimeField(auto_now_add=True)
# 	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
# 	active = models.BooleanField(default=True)

class Message(models.Model):
	# inquiry = models.ManyToManyField(Inquiry)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')        
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')        
	message = models.CharField(max_length=1200)
	timestamp = models.DateTimeField(auto_now_add=True)
	fk_message_parent = models.ForeignKey('Message',  related_name="parent_message", on_delete=models.CASCADE, null=True, blank=True)
	is_read = models.BooleanField(default=False)

	def __str__(self):
	   return self.message
	class Meta:
	   ordering = ('timestamp',)

	# def remove(self):
	# 	return self.item.remove_from_cart()


# def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
# 	qty = instance.quantity
# 	if Decimal(qty) >= 1:
# 		price = instance.item.get_price()
# 		line_item_total = Decimal(qty) * Decimal(price)
# 		instance.line_item_total = line_item_total

# pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)



# def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
# 	instance.cart.update_subtotal()

# post_save.connect(cart_item_post_save_receiver, sender=CartItem)

# post_delete.connect(cart_item_post_save_receiver, sender=CartItem)



	# discounts
	# shipping

	# def __unicode__(self):
	# 	return str(self.id)

	# def update_subtotal(self):
	# 	print("updating...")
	# 	subtotal = 0
	# 	items = self.cartitem_set.all()
	# 	for item in items:
	# 		subtotal += item.line_item_total
	# 	self.subtotal = "%.2f" %(subtotal)
	# 	self.save()

	# def is_complete(self):
	# 	self.active = False
	# 	self.save()
