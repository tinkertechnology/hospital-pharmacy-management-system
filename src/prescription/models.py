from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Prescription(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=100) #name is filename without extension
    version = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    size = models.IntegerField(default=0)