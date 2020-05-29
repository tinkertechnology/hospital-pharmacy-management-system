from rest_framework import serializers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import MembershipType, UserMembership
# from carts.models import Cart #importing from other folders

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

		db_membership = UserMembership.objects.filter(fk_member_user_id = user.id).first()
		if( db_membership != None): #dont create new if membership already exists
			return db_membership;
		

		print(validated_data)
		u = UserMembership()
		u.fk_member_user_id = user.id
		u.fk_membership_type = validated_data.get('fk_membership_type')
		u.save()
		
		return u
	
	class Meta:
		model = UserMembership
		fields= '__all__'