from rest_framework import serializers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Store

from orders.models import StoreWiseOrder

class StoreSerializer(serializers.ModelSerializer):
	distance =  serializers.FloatField(required=False)
	class Meta:
		model = Store
		fields= '__all__'


class StoreWiseOrderSerializer(serializers.ModelSerializer):
	distance =  serializers.FloatField(required=False)
	class Meta:
		model = Store
		fields= '__all__'


class StoreUserTypeSerializer(serializers.ModelSerializer):
	# store = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields =['username', 'mobile', 'email']

		def get_store(self, obj):
			print(obj.id)
			# depo =  StoreUser.objects.filter(fk_user_id=obj.id).first()
			# return depo.fk_store_id 
	# def get_queryset(self,obj):
	# 	return obj.all()
	# def get_contact(self,obj):
	# 	print(obj.id)
	# 	return obj.mobile