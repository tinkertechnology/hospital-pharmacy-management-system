# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
# from wsc.models import WaterSupplyCompany
from store.models import Store
from users.models import UserType, UserTypes
from django.conf import settings
from datetime import date
from django.db.models import Q
from model_utils import Choices
from counter.models import Counter
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
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
	title = models.CharField(max_length=120)
	active = models.BooleanField(default=True)
	fk_user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True) #for patient type drug filter
	rack_number = models.CharField(max_length=120, null=True, blank=True)
	code = models.CharField(max_length=120, null=True, blank=True)
	categories = models.ManyToManyField('Category', blank=True)
	brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=True, null=True)
	generic_name = models.ForeignKey('GenericName', on_delete=models.CASCADE, blank=True, null=True)
	company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)	
	alert_quantity = models.DecimalField(decimal_places=2, max_digits=20, default=20, null=True)
	alert_expiry_days = models.DecimalField(decimal_places=2, max_digits=20, default=20, null=True)
	fk_counter = models.ForeignKey(Counter, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		return self.title

	


ORDER_COLUMN_CHOICES = Choices(
	('0', 'id'),
	('1', 'song'),
	('2', 'singer'),
	('3', 'last_modify_date'),
	('4', 'created'),
)

# from orders.models import PurchaseItem
class VariationBatch(models.Model):
	fk_variation = models.ForeignKey(Variation, on_delete=models.CASCADE,)
	fk_purchaseitem = models.ForeignKey("orders.PurchaseItem", on_delete=models.CASCADE, null=True)
	quantity = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	batchno = models.CharField(max_length=100, null=True, blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	created_at = models.DateField(default=date.today)
	expiry_date = models.DateField(null=True, blank=True)
	purchase_date = models.DateField(null=True, blank=True)
	use_batch = models.BooleanField(default=True)

	def __str__(self):
		return '%s-%s' %(self.fk_variation.title, self.batchno)

def query_musics_by_args(**kwargs):
	draw = int(kwargs.get('draw', None)[0])
	length = int(kwargs.get('length', None)[0])
	start = int(kwargs.get('start', None)[0])
	search_value = kwargs.get('search[value]', None)[0]
	order_column = kwargs.get('order[0][column]', None)[0]
	order = kwargs.get('order[0][dir]', None)[0]

	order_column = ORDER_COLUMN_CHOICES[order_column]
	# django orm '-' -> desc
	if order == 'desc':
		order_column = '-' + order_column

	queryset = VariationBatch.objects.all()
	total = queryset.count()

	if search_value:
		queryset = queryset.filter(Q(id__icontains=search_value) |
										Q(song__icontains=search_value) |
										Q(singer__icontains=search_value) |
										Q(last_modify_date__icontains=search_value) |
										Q(created__icontains=search_value))

	count = queryset.count()
	queryset = queryset.order_by(order_column)[start:start + length]
	return {
		'items': queryset,
		'count': count,
		'total': total,
		'draw': draw
	}




class VariationPrice(models.Model):
	fk_user_type = models.ForeignKey(UserTypes, on_delete=models.CASCADE, null=True) #for patient type drug filter
	fk_variation = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20, null=True)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)

class VariationBatchPrice(models.Model):
	fk_user_type = models.ForeignKey(UserTypes, on_delete=models.CASCADE, null=True) #for patient type drug filter
	fk_variation_batch = models.ForeignKey(VariationBatch, on_delete=models.CASCADE, null=True) #for patient type drug filter
	price = models.DecimalField(decimal_places=2, max_digits=20, null=True)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)

	def __str__(self):
		return 'batch number :%s for Patient-type-[%s]-price-%s' %(self.fk_variation_batch.batchno, self.fk_user_type.title, self.price)



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
		# if product.price:
		# 	new_var.price = product.price
		new_var.price = 0
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









