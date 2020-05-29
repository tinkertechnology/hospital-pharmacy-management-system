from rest_framework import serializers
from .models import  UserType, UserTypes
from django.conf import settings
from django.contrib.auth.models import User
from inquiry.models import Message
from django.db.models import Q, Count


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = '__all__'


class InqueryUserSerializer(serializers.ModelSerializer):
	# image_url = serializers.SerializerMethodField('get_image_url')
	user = serializers.SerializerMethodField()
	class Meta:
		model = UserType
		fields = [
		"id",
		"user_id",
		"user_type",
		"user"

		]

	def get_user(self,obj):
		get_user = User.objects.get(pk=obj.user_id)
		user_dict = {
			"first_name": get_user.first_name,
			"last_name" : get_user.last_name,
			"username": get_user.username,
			"email": get_user.email
		}
		return user_dict

class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "first_name"]




class InquiryUsersListForPharmacistSerializer1(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	class Meta:
		model = Message
		fields = [
		
		"user"

		]


	def get_user(self, obj)	:
		user =  self.context['request'].user
		#inquired_users = {}
		qs =  User.objects.raw('select DISTINCT sender_id as id FROM inquiry_message WHERE receiver_id=3')#Message.objects.filter(receiver_id=user.id).values('sender_id').annotate(sender_id_count=Count('sender_id')).distinct()
		#print(inquired_users)
		#selected_items = Message.objects.all().filter(receiver_id=user.id).distinct('sender_id')
		sender = []

		for u in qs:
			sender.append({'id' : u.id, 'name' : u.first_name})


		return sender
		u = InqueryUserSerializer(qs, many=True, read_only=True)

		print(u)
		return u 



class InquiryUsersListForPharmacistSerializer(serializers.ModelSerializer):
	#user = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = [
		
		"id",
		"first_name",
		"last_name",
		"username",
		"email"

		]


	


	# def get_user(self,obj):
	# 	usertype_title = UserTypes.objects.get(obj.user_type_id=id).first()
	# 	return usertype_title




	# def create(self,validated_data):
	# 	inquery = Message()
	# 	receiver_user = User.objects.get(pk=17)

	# 	datas = {
	# 		"sender": self.context['request'].user,
	# 		"receiver" : receiver_user,
	# 		"message" : validated_data['message']
	# 	}

	# 	messages= Message.objects.create(**datas)

	# 	return messages


