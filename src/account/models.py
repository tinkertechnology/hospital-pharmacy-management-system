from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

class MyAccountManager(BaseUserManager):
	def create_user(self,email,mobile, username, password=None):
		if not mobile:
			raise ValueError('Users must have an mobile number')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			mobile=self.normalize_email(mobile),
			username=username,
			email=email
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,mobile, email, username, password):
		user = self.create_user(
			mobile=self.normalize_email(mobile),
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
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	mobile 					= models.CharField(max_length=30, unique=True)


	USERNAME_FIELD = 'mobile'
	REQUIRED_FIELDS = ['username', 'email']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def __str__(self):
		return self.mobile

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


class PhoneOTP(models.Model):
	phone_regex = RegexValidator( regex =r'^\+?1?\d{9,14}$', message="phone number must be entered in the form of....")
	mobile = models.CharField(validators=[phone_regex], max_length=17, unique=True)
	otp = models.CharField(max_length=9, blank=True, null=True)
	count = models.IntegerField(default=0, help_text='No. of otp sent')

	def __str__(self):
		return str(self.mobile) + 'is sent' +str(self.otp)










