from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Store(models.Model):
    fk_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fk_user', on_delete=models.CASCADE, blank=True)
    is_active = models.IntegerField(null=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
    	return self.title