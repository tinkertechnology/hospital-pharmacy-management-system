from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

class MyAccountManager(BaseUserManager):
	def create_user(self,email,mobile, username, password=None):
		if not mobile:
			raise ValueError('Users must have an mobile number')
		# if not username:
		# 	raise ValueError('Users must have a username')
		if not username:
			username = mobile

		user = self.model(
			mobile=self.normalize_email(mobile),
			username=username,
			email=email,
			password=password
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,mobile, email, username, password):
		user = self.create_user(
			mobile=mobile,
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+977999999'. Up to 15 digits allowed.")
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	firstname				= models.CharField(max_length=100)
	lastname				= models.CharField(max_length=100)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	mobile 					= models.CharField(validators=[phone_regex],max_length=15, unique=True)
	nick_name 				= models.CharField(max_length=100, null=True, blank=True)
	firebase_token          = models.CharField(max_length=500, null=True, blank=True)


	USERNAME_FIELD = 'mobile'
	REQUIRED_FIELDS = ['username', 'email']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def __str__(self):
		return  self.mobile + self.email + self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


class PhoneOTP(models.Model):
	phone_regex = RegexValidator( regex =r'^\+?1?\d{9,14}$', message="phone number must be entered in the format: '+97799999'. Up to 15 digits allowed")
	mobile = models.CharField(validators=[phone_regex], max_length=15, unique=True)
	otp = models.CharField(max_length=9, blank=True, null=True)
	count = models.IntegerField(default=0, help_text='No. of otp sent')
	validated = models.BooleanField(default=False, help_text='if true, user validated otp in secount api')

	def __str__(self):
		return str(self.mobile) + 'is sent' +str(self.otp)



class PasswordResetOTP(models.Model):
	phone_regex = RegexValidator( regex =r'^\+?1?\d{9,14}$', message="phone number must be entered in the format: '+97799999'. Up to 15 digits allowed")
	mobile = models.CharField(validators=[phone_regex], max_length=15, unique=True)
	otp = models.CharField(max_length=9, blank=True, null=True)
	count = models.IntegerField(default=0, help_text='No. of otp sent')
	validated = models.BooleanField(default=False, help_text='if true, user validated otp in secount api')

	def __str__(self):
		return str(self.mobile) + 'is sent' +str(self.otp)

class CustomerRegisterSurvey(models.Model):
	mobile = models.CharField(max_length=100, blank=True, null=True)
	firstname = models.CharField(max_length=100, blank=True, null=True)
	lastname = models.CharField(max_length=100, blank=True, null=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	email = models.CharField(max_length=100, blank=True, null=True)
	know_about_us = models.CharField(max_length=100, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class CustomerDepotRequest(models.Model):
	mobile = models.CharField(max_length=100, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	message = models.CharField(max_length=500, blank=True, null=True)

class CustomerMessage(models.Model):
	message = models.CharField(max_length=500, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return str(self.message)

class CallLog(models.Model):
	number = models.CharField(max_length=10, null=True, blank=True)
	is_existing = models.BooleanField(default=False)
	timestamp = models.DateTimeField(verbose_name='call timestamp', auto_now_add=True)
	timestamp_str = models.CharField(max_length=100, blank=True, null=True)
	timestamp_i64 = models.BigIntegerField(null=True, blank=True)
	def __str__(self):
		return self.number