from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()


class Prescription(models.Model):
    file = models.FileField(upload_to="Prescription")
    name = models.CharField(max_length=100) #name is filename without extension
    version = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    doctor_name = models.CharField(max_length=200, null=True, blank=True)
    hospital_name = models.CharField(max_length=200, null=True, blank=True)
    size = models.IntegerField(default=0)