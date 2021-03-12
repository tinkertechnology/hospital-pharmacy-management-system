from django.db import models

# Create your models here.
class PaymentMethod(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    code = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
    	return self.title