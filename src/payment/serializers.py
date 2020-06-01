from rest_framework import serializers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import PaymentMethod

class PaymentMethodSerializer(serializers.ModelSerializer):
	class Meta:
		model = PaymentMethod
		fields= '__all__'