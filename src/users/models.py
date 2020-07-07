from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

from django.conf import settings
from django.db import models



class UserTypes(models.Model):
	title = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.title)
	


class UserType(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	user_type = models.ForeignKey(UserTypes, on_delete=models.CASCADE, null=True, blank=True, default=2)

	def __str__(self):
		return str(self.user.mobile+ self.user_type.title)
	# def __str__(self):
	# 	if self.user is None and self.user_type is None:
	# 		return "User's type not set"
	# 	return str(self.user+ self.user_type.title)








    


