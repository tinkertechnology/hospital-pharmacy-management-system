from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Slider(models.Model):
	is_active = models.IntegerField(null=True)
	title = models.CharField(max_length=500, null=True, blank=True)
	slider_file = models.FileField(upload_to="slider_images")
	upload_date = models.DateTimeField(auto_now=True, db_index=True)

	def __str__(self):
		return self.title
# Create your models here.
