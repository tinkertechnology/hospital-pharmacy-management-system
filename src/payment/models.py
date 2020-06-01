from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class PaymentMethod(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
    	return self.title