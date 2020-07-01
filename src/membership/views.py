from django.shortcuts import render
from .serializers import MembershipTypeSerializer, UserMembershipSerializer, UserMembershipAutoOrderSerializer
from .models import MembershipType, UserMembership, UserMembershipAutoOrder

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

#http://localhost:8000/api/membership-type/
class MembershipTypeListCreateApiView(ListCreateAPIView):
    serializer_class = MembershipTypeSerializer

    def get_queryset(self, *args, **kwargs):
        #return Order.objects.filter(user__user=self.request.user)
        return MembershipType.objects.all()

#http://localhost:8000/api/membership-type/<pk>/
#
class MembershipTypeRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = MembershipTypeSerializer
    def get_queryset(self, *args, **kwargs):
        return MembershipType.objects.all()

#http://localhost:8000/api/user-membership/
class UserMembershipListCreateApiView(ListCreateAPIView):
    serializer_class = UserMembershipSerializer

    def get_queryset(self, *args, **kwargs):
        return UserMembership.objects.all()

#http://localhost:8000/api/user-membership/<pk>/
class UserMembershipRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserMembershipSerializer

    def get_queryset(self, *args, **kwargs):
        return UserMembership.objects.all()

#for logged in user
#http://localhost:8000/api/user-membership-retrieve/
class UserMembershipRetrieveApiView(RetrieveAPIView):
    serializer_class = UserMembershipSerializer

    def get_queryset(self, *args, **kwargs):
        return UserMembership.objects.all()
    
    # need to override get_object(), not get_queryset() for detail views.
    def get_object(self):
        print (self.request.user.__dict__)
        print (self.request.user.id)
        #return None
        
        #queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        #obj = queryset.get(pk=self.request.user.id)
        #self.check_object_permissions(self.request, obj)
        obj = UserMembership.objects.filter(fk_member_user_id=self.request.user.id).first()
        print(obj.__dict__)
        if(obj):
            print(obj.__dict__)
            #return UserMembership()
        return obj

# https://stackoverflow.com/questions/43859053/django-rest-framework-assertionerror-fix-your-url-conf-or-set-the-lookup-fi


#http://localhost:8000/api/user-membership/
class UserMembershipAutoOrderListCreateApiView(ListCreateAPIView):
    serializer_class = UserMembershipAutoOrderSerializer

    def get_queryset(self, *args, **kwargs):
        return UserMembershipAutoOrder.objects.all()