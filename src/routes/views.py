from django.shortcuts import render
from .serializers import RouteSerializer, RouteDetailSerializer
from .models import Route, RouteDetail
from store.models import Store

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


class StoreWiseRouteListApiView(ListAPIView):
    serializer_class = RouteSerializer

    def get_queryset(self, *args, **kwargs):
        store = Store.objects.filter(fk_user_id=self.request.user.id).first()
        print(store)
        storewise_route = Route.objects.filter(fk_store_id=store.id)
        print(storewise_route)

        return storewise_route

    

