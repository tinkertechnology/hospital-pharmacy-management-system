# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
# from wsc.models import WaterSupplyCompany
from store.models import Store
from users.models import UserType
from django.conf import settings
# Create your models here.

class ProductQuerySet(models.query.QuerySet):
	def active(self): 
		return self.filter(active=True)


class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return self.get_queryset().active()

	def get_related(self, instance):
		products_one = self.get_queryset().filter(categories__in=instance.categories.all())
		products_two = self.get_queryset().filter(default=instance.default)
		qs = (products_one | products_two).exclude(id=instance.id).distinct()
		return qs

def common_product_lab_report_upload_to(instance, filename):
	title = instance.title
	basename, file_extension = filename.split(".")
	new_filename = "%s/%s.%s.%s" %(instance.title,instance.id, instance.title, file_extension)
	return "lab_report_file/%s" %(new_filename)

class ProductCommon(models.Model):
	title = models.CharField(max_length=120, null=True, blank=True)
	lab_report_file = models.FileField(upload_to=common_product_lab_report_upload_to, null=True, blank=True)
	def __str__(self):
		return self.title



class Product(models.Model):
	fk_common_product = models.ForeignKey(ProductCommon, on_delete=models.CASCADE, null=True, blank=True)
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	# price = models.DecimalField(decimal_places=2, max_digits=20)
	active = models.BooleanField(default=True)
	categories = models.ManyToManyField('Category', blank=True)
	brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=True, null=True)
	generic_name = models.ForeignKey('GenericName', on_delete=models.CASCADE, blank=True, null=True)
	company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)
	amount = models.FloatField(null=True, default=0.0, blank=True)
	product_unit = models.ForeignKey('ProductUnit', on_delete=models.CASCADE, blank=True, null=True)
	fk_store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=True, null=True)
	is_featured = models.BooleanField(default = False, blank=True)
	#Store najik navayeni saman jata pani availalbe huncha, 
	#latitude ,longitude depo ko check nagareko
	can_sell_everywhere = models.BooleanField(default=False, blank=True) 
	default = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='default_category', null=True, blank=True)

	# can only ordered  by internal staff
	# not visible by app
	is_internal = models.BooleanField(default=False) 

	objects = ProductManager()

	class Meta:
		ordering = ["-title"]

	def __str__(self): #def __str__(self):
		# return 'jpt'
		store = self.fk_store
		print(store)
		# print(self)
		if store:
			return self.title +'. '+store.title
		return self.title


	def get_absolute_url(self):
		return reverse("product_detail", kwargs={"pk": self.pk})

	def get_image_url(self):
		img = self.productimage_set.first()
		if img:
			return img.image.url
		return img #None

class Variation(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE,)
	title = models.CharField(max_length=120)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True) #refer none == unlimited amount
	is_refill = models.BooleanField(default=False)
	keep_stock = models.BooleanField(default=False)
	fk_user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True) #for patient type drug filter
	expiry_date = models.DateField(null=True, blank=True)
	# can only ordered  by internal staff
	# not visible by app
	is_internal = models.BooleanField(default=False) 

	def __str__(self):
		return self.title

	def get_price(self):
		if self.sale_price is not None:
			return self.sale_price
		else:
			return self.price

	def get_html_price(self):
		if self.sale_price is not None:
			html_text = "<span class='sale-price'>%s</span> <span class='og-price'>%s</span>" %(self.sale_price, self.price)
		else:
			html_text = "<span class='price'>%s</span>" %(self.price)
		return mark_safe(html_text)

	def get_absolute_url(self):
		return self.product.get_absolute_url()

	def add_to_cart(self):
		return "%s?item=%s&qty=1" %(reverse("cart"), self.id)

	def remove_from_cart(self):
		return "%s?item=%s&qty=1&delete=True" %(reverse("cart"), self.id)

	def get_title(self):
		return "%s - %s" %(self.product.title, self.title)
	

from datetime import date
class UserVariationQuantityHistory(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="jar_users", on_delete=models.CASCADE, null=True, blank=True)
	variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
	num_taken = models.FloatField(default=0)
	num_returned = models.FloatField(default=0)
	num_delta = models.FloatField(default=0)
	comment = models.CharField(max_length=500, null=True, blank=True)
	timestamp = models.DateField(default=date.today)

def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
	product = instance
	variations = product.variation_set.all()
	if variations.count() == 0:
		new_var = Variation()
		new_var.product = product
		new_var.title = "Default"
		new_var.price = product.price
		new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)


def image_upload_to(instance, filename):
	title = instance.product.title
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
	return "products/%s/%s" %(slug, new_filename)


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(upload_to=image_upload_to)

	def __str__(self):
		return self.product.title

# Product Category


def category_image(instance, filename):
	title = instance.title
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
	return "category_images/%s/%s" %(slug, new_filename)

class Category(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	fk_category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	image = models.ImageField(upload_to=category_image, null=True, blank=True)

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("category_detail", kwargs={"slug": self.slug })



class GenericName(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.title

class ProductUnit(models.Model):
	title = models.CharField(max_length=120, unique=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.title
	# def get_absolute_url(self):
	# 	return reverse("category_detail", kwargs={"slug": self.slug })


class Brand(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.title



class Company(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.title		

def image_upload_to_featured(instance, filename):
	title = instance.product.title
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
	return "products/%s/featured/%s" %(slug, new_filename)




class ProductFeatured(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(upload_to=image_upload_to_featured)
	title = models.CharField(max_length=120, null=True, blank=True)
	text = models.CharField(max_length=220, null=True, blank=True)
	text_right = models.BooleanField(default=False)
	text_css_color = models.CharField(max_length=6, null=True, blank=True)
	show_price = models.BooleanField(default=False)
	make_image_background = models.BooleanField(default=False)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.product.title









