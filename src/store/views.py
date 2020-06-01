from django.shortcuts import render
from .serializers import StoreSerializer
from .models import Store

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

#http://localhost:8000/api/store/
class StoreListCreateApiView(ListCreateAPIView):
    serializer_class = StoreSerializer

    def get_queryset(self, *args, **kwargs):
        return Store.objects.all()

#http://localhost:8000/api/store/<pk>/
#
class StoreRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = StoreSerializer
    def get_queryset(self, *args, **kwargs):
        return Store.objects.all()
