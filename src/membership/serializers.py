from rest_framework import serializers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import MembershipType, UserMembership, UserMembershipAutoOrder
from products.serializers import VariationSerializer
# from carts.models import Cart #importing from other folders
from django.contrib.auth import get_user_model
User = get_user_model()

class MembershipTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = MembershipType
		fields= '__all__'

class UserMembershipSerializer(serializers.ModelSerializer):

	is_active_str = serializers.SerializerMethodField()
	def get_is_active_str(self, obj):
		is_active="Not Activated";
		if(obj.is_active):
			is_active = "Activated";
		return is_active;
	
	def create(self, validated_data):
		user =  self.context['request'].user
		membership_user = user
		print(validated_data)
		print(user)

		if(user.is_superuser): # superuser le jallai ni banauna paucha member
			fk_member_user_id = validated_data.get('fk_member_user').id
			membership_user = User.objects.filter(pk=fk_member_user_id).first()

		db_membership = UserMembership.objects.filter(fk_member_user_id = membership_user.id).first()
		if( db_membership != None): #dont create new if membership already exists
			u = db_membership
		else:
			u = UserMembership()
	
		u.fk_member_user_id = membership_user.id
		u.fk_membership_type = validated_data.get('fk_membership_type')
		u.is_active = validated_data.get('is_active')
		u.is_auto_order = validated_data.get('is_auto_order')
		u.auto_order_duration = validated_data.get('auto_order_duration')
		u.save()
		
		return u
	
	class Meta:
		model = UserMembership
		fields= '__all__'

class UserMembershipAutoOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserMembershipAutoOrder
		fields= '__all__'


class UserMembershipUserAutoOrdersListSerializer(serializers.ModelSerializer):
	fk_variation = VariationSerializer()
	fk_usermembership = UserMembershipSerializer()
	class Meta:
		model = UserMembershipAutoOrder
		fields= '__all__'



