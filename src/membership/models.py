from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class MembershipType(models.Model):
    type_name= models.CharField(max_length=100)
    #todo: add duration

class UserMembership(models.Model):
    fk_member_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fk_member_user', on_delete=models.CASCADE, blank=True)
    is_active = models.IntegerField(null=True)
    start_date = models.DateTimeField(auto_now_add=True) # when created
    fk_membership_type = models.ForeignKey(MembershipType, related_name='fk_membership_type', on_delete=models.CASCADE)