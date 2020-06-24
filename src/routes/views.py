from django.shortcuts import render
from .serializers import RouteSerializer, RouteDetailSerializer
from .models import Route, RouteDetail

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

#http://localhost:8000/api/route/
class RouteListCreateApiView(ListCreateAPIView):
    serializer_class = RouteSerializer

    def get_queryset(self, *args, **kwargs):
        return Route.objects.all()

#http://localhost:8000/api/route/<pk>/
#
class RouteRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = RouteSerializer
    def get_queryset(self, *args, **kwargs):
        return Route.objects.all()

# http://localhost:8000/api/routedetail/
class RouteDetailListCreateApiView(ListCreateAPIView):
    serializer_class = RouteDetailSerializer

    def get_queryset(self, *args, **kwargs):
        return RouteDetail.objects.all()

# http://localhost:8000/api/routedetail/<pk>/
#
class RouteDetailRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = RouteDetailSerializer
    def get_queryset(self, *args, **kwargs):
        return RouteDetail.objects.all()
