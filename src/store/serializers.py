from rest_framework import serializers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Store

class StoreSerializer(serializers.ModelSerializer):
	distance =  serializers.FloatField(required=False)
	class Meta:
		model = Store
		fields= '__all__'