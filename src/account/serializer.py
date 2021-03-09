from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Account

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('mobile', 'password', 'email', 'username', 'firstname','lastname', 'nick_name')
		extra_kwargs = {'password': {'write_only': True}, }


	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
			instance.save()
		return instance

	def update(self, instance, validated_data):
		for attr, value in validated_data.items():
			if attr == 'password':
				instance.set_password(value)
			else:
				setattr(instance, attr, value)
		instance.save()
		return instance
		# def create(self, validated_data):

class UpdateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model =User
		fields = ['password']

	
	def update(self, instance, validated_data):
		
		for attr, value in validated_data.items():
			if attr == 'password':
				instance.set_password(value)
			else:
				setattr(instance, attr, value)

		instance.save()
		return instance





class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['firstname','lastname']
		


			# password = serializers.CharField(write_only=True)

			# def create(self, validated_data):
			# 	user = User.objects.create_user(
			# 	username=validated_data['username'],
			# 	password=validated_data['password'],
			# 	mobile=validated_data['mobile'],
			# 	email=validated_data['email'],
			# 	)
			# 	return user

			# password = validated_data.pop('password')
			# user = super().create(validated_data)
			# user.set_password(make_password(validated_data['password']))
			# # user = Account.objects.create(**validated_data)
			# user.save()
			# return user
			# user = User(**validated_data)
			# # Hash the user's password.
			# user.set_password(validated_data['password'])
			# user.save()
			# return user
# from store.models import StoreAccount
from products.serializers import UserVariationQuantityHistorySerializer
from products.models import UserVariationQuantityHistory
from carts.models import Comment
from carts.serializers import CommentSerializer
# from store.service import getUserStoreService
from store.models import StoreUser
from users.serializers import DeliveryUserSerializer

class UserSerializer(serializers.ModelSerializer):
	credit = serializers.SerializerMethodField()
	jardetails = serializers.SerializerMethodField()
	# delivery_boys = serializers.SerializerMethodField()
	comments = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ('firstname', 'lastname','mobile', 'nick_name', 'credit', 'jardetails',"comments")

	def get_credit(self, obj):
		user = StoreAccount.objects.filter(fk_user=obj).first()
		if user:
			return user.credit
		return ''
	def get_jardetails(self, obj):
		jardetails = UserVariationQuantityHistorySerializer(UserVariationQuantityHistory.objects.filter(user=obj), many=True)
		return jardetails.data
	
	def get_comments(self, obj):
		comments = CommentSerializer(Comment.objects.filter(user=obj), many=True)
		return comments.data
	
from products.models import Variation
from products.serializers import ProductVariationListSerializer		
from datetime import datetime



from users.models import UserType

class UserTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserType
		fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
	patient_type = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ['id','firstname','lastname', 'mobile', 'patient_type']

	def get_patient_type(self, obj):
		ptype =  UserType.objects.filter(user=obj).first()
		data = {}
		if ptype:
			data = {
				'p_type_id': ptype.user_type.id,
				'p_type_title' : ptype.user_type.title
			}
		return data
		# return UserTypeSerializer(ptypes, read_only=True).data
from .models import Doctor, Visit
class DoctorSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'firstname', 'lastname', 'mobile']

class VisitSeriailizer(serializers.ModelSerializer):
	class Meta:
		model = Visit
		fields ='__all__'
