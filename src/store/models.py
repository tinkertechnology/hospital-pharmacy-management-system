from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
# from routes.models import Route
from users.models import UserTypes
User = get_user_model()

class StoreType(models.Model):
	title = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.title
# Create your models here.
class Store(models.Model):
    fk_store_type = models.ForeignKey(StoreType, null=True, blank=True, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fk_user', on_delete=models.CASCADE, blank=True)
    is_active = models.IntegerField(null=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
    	return self.title

class StoreUser(models.Model):
    fk_store = models.ForeignKey(Store, null=True, blank=True, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    fk_store_usertypes = models.ForeignKey(UserTypes, null=True, blank=True, on_delete=models.CASCADE) #Delivery/Manager
    # fk_route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=True)

    