from django.shortcuts import render
from rest_framework.generics import *
from rest_framework import permissions
from django.conf import settings
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

# from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .models import Message

# Create your views here.
from .serializers import InquirySerializer, MessageSerializer, MessageViewSerializer

# @csrf_exempt
class InquiryApiView(CreateAPIView):
	model = Message
	serializer_class = InquirySerializer
	permission_classes = [permissions.IsAuthenticated]


def message_list(request, sender=None, receiver=None):
	if request.method == 'GET':
		messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)
		serializer = MessageSerializer(messages, many=True, context={'request': request})
		print(serializer.__dict__)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = MessageSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	return JsonResponse(serializer.errors, status=400)

class view_messages(ListAPIView):
	model = Message
	serializer_class = MessageViewSerializer

	def get_queryset(self, *args, **kwargs):
		user =  self.request.user
		receiver = self.request.GET.get("receiver")
		print(receiver)
		m = Message.objects.filter(sender_id=user, receiver_id=receiver) | Message.objects.filter(sender_id=receiver, receiver_id=user)
		print(m.query)
		return m 




