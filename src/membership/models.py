from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

from products.models import Variation


# Create your models here.
class MembershipType(models.Model):
    type_name= models.CharField(max_length=100)
    #todo: add duration

class UserMembership(models.Model):
    fk_member_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fk_member_user', on_delete=models.CASCADE, blank=True)
    is_active = models.IntegerField(null=True)
    start_date = models.DateTimeField(auto_now_add=True) # when created
    fk_membership_type = models.ForeignKey(MembershipType, related_name='fk_membership_type', on_delete=models.CASCADE)
    is_auto_order = models.IntegerField(null=True)
    auto_order_duration = models.IntegerField(null=True)


class UserMembershipAutoOrder(models.Model):
	fk_usermembership = models.ForeignKey(UserMembership, on_delete=models.CASCADE);
	fk_variation = models.ForeignKey(Variation, on_delete=models.CASCADE);
	quantity = models.PositiveIntegerField(default=1)
