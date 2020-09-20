from rest_framework import serializers
from .models import  Message
from django.conf import settings
# from django.contrib.auth.models import User
from account.models import Account
from django.contrib.auth import get_user_model
import time
User = get_user_model()




class InquirySerializer(serializers.ModelSerializer):
	# image_url = serializers.SerializerMethodField('get_image_url')
	# user = serializers.SerializerMethodField('_user')

	class Meta:
		model = Message
		fields = '__all__'


	def create(self,validated_data):
		inquery = Message()
		# receiver_user_id = self.context['request'].POST.get("receiver")
		# receiver = User.objects.get(pk=receiver_user_id)
		#receiver_user = User.objects.get(pk=self.context['request'].GET.get("receiver"))

		datas = {
			"sender": self.context['request'].user,
			"receiver" : validated_data['receiver'],
			"message" : validated_data['message']
		}

		messages= Message.objects.create(**datas)

		return messages

# class InquirySerializer(serializers.ModelSerializer):
# 	# image_url = serializers.SerializerMethodField('get_image_url')
# 	# user = serializers.SerializerMethodField('_user')

# 	class Meta:
# 		model = Message
# 		fields = '__all__'


# 	def create(self,validated_data):
# 		inquery = Message()
# 		#receiver_user_id = self.context['request'].POST.get("receiver")
# 		#receiver_user = User.objects.get(pk=self.context['request'].GET.get("receiver"))
# 		order = StoreWiseOrder.objects.get(pk=self.context['request'].GET.get("order_id"))
# 		message = self.context['request'].GET.get("message")
# 		if order:
# 			receiver = order.fk_auth_user_id

# 			datas = {
# 				"sender": self.context['request'].user,
# 				"receiver" : receiver,
# 				"message" : validated_data['message']
# 			}

# 			messages= Message.objects.create(**datas)

# 			return messages



# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
	"""For Serializing Message"""
	sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
	receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
	sent_date = serializers.SerializerMethodField('get_timestamp')
	class Meta:
		model = Message
		fields = ['sender', 'receiver', 'message', 'timestamp']

class MessageViewSerializer(serializers.ModelSerializer):
	messages = serializers.SerializerMethodField()
	response_date = serializers.SerializerMethodField('get_timestamp')
	class Meta:
		model = Message
		fields = ['sender', 'receiver', 'message', 'timestamp', 'messages', 'response_date']

	

	def get_messages(self, request):
		user =  self.context['request'].user
		receiver = self.context['request'].GET.get("receiver")
		return receiver


	def get_timestamp(self, obj):
	#times 1000 for javascript.
		return time.mktime(obj.timestamp.timetuple()) * 1000













