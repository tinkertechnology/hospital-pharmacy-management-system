from django.db import models


# Create your models here.
class AppSettings(models.Model):
	# todo disable auto increment on app settings
	# or auto increase  app settings
	# or manual input to id
	id = models.IntegerField(primary_key=True)
	group = models.IntegerField(null=True, blank=True)
	key = models.CharField(max_length=100, blank=True)
	value = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.key + self.value


class SideMenu(models.Model):
	title = models.CharField(max_length=100, null=True, blank=True)
	order = models.FloatField(null=True)
	parent_id = models.ForeignKey('SideMenu', on_delete=models.CASCADE, null=True, blank=True)
	url = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.title)

class FiscalYear(models.Model):
	title =models.CharField(max_length=100, null=True, blank=True)
	active = models.BooleanField(default=False, null=True, blank=True)
	
	def __str__(self):
		return self.title