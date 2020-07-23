from rest_framework import serializers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from store.models import StoreUser
from users.serializers import UserSerializer
from routes.serializers import RouteSerializer
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
	route_id = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields =['username', 'mobile', 'email', 'route_id']

	def get_route_id(self, obj):
		print(obj.id)
		route = StoreUser.objects.filter(fk_user_id=obj.id).first()
		print(route)
		return route.id
			# depo =  StoreUser.objects.filter(fk_user_id=obj.id).first()
			# return depo.fk_store_id 
	# def get_queryset(self,obj):
	# 	return obj.all()
	# def get_contact(self,obj):
	# 	print(obj.id)
	# 	return obj.mobile


class StoreUserListSerializer(serializers.ModelSerializer):
	fk_user = UserSerializer()
	fk_store = StoreSerializer()
	fk_route = RouteSerializer()
	class Meta:
		model = StoreUser
		fields = '__all__'


