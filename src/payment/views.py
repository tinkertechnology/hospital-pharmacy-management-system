from django.shortcuts import render
from .serializers import PaymentMethodSerializer
from .models import PaymentMethod

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

#http://localhost:8000/api/PaymentMethod/
class PaymentMethodListCreateApiView(ListCreateAPIView):
    serializer_class = PaymentMethodSerializer

    def get_queryset(self, *args, **kwargs):
        return PaymentMethod.objects.all()

#http://localhost:8000/api/PaymentMethod/<pk>/
#
class PaymentMethodRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentMethodSerializer
    def get_queryset(self, *args, **kwargs):
        return PaymentMethod.objects.all()
