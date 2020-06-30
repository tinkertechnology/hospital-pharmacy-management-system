from django.shortcuts import render
from .serializers import StoreSerializer, StoreUserTypeSerializer
from .models import Store, StoreUser

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User = get_user_model()
#https://stackoverflow.com/questions/19703975/django-sort-by-distance
from django.db import models
from django.db.models.expressions import RawSQL
from django.db.models.functions import Greatest

def get_locations_nearby_coords(latitude, longitude, max_distance=None):
    """
    Return objects sorted by distance to specified coordinates
    which distance is less than max_distance given in kilometers
    """
    # Great circle distance formula
    gcd_formula = """
	    6371 * 
	        acos(
	            cos( radians( %s ) ) * cos( radians( latitude ) ) * cos ( radians(longitude) - radians(%s) ) +
	            sin( radians(%s) ) * sin( radians( latitude ) )
	        )
    """ % (latitude, longitude, latitude) 

    distance_raw_sql = RawSQL(
        gcd_formula,
        ()
    )
    qs = Store.objects.all() \
    .annotate(distance=distance_raw_sql)\
    .order_by('distance')
    if max_distance is not None:
    	qs = qs.filter( distance__lt= float(max_distance) )


    print(qs.query)
    print(qs.all())
    return qs


#http://localhost:8000/api/store/
#rk
#http://localhost:8000/api/store/?ulat=27.665692&ulng=85.425633&r=99&get_nearest=true
#sunil
#http://localhost:8000/api/store/?ulat=27.73007128&ulng=85.35944362&r=99&get_nearest=true
class StoreListCreateApiView(ListCreateAPIView):
    serializer_class = StoreSerializer

    def get_queryset(self, *args, **kwargs):
        ulat = self.request.GET.get("ulat")
        ulng = self.request.GET.get("ulng")
        r = self.request.GET.get("r")
        get_nearest = self.request.GET.get("get_nearest")

        print(ulat, ulng, r)
        if get_nearest:
        	#q = Store.objects.all()
        	qs = get_locations_nearby_coords(ulat, ulng, r)
        	return qs

        return Store.objects.all()

#http://localhost:8000/api/store/<pk>/
#
class StoreRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = StoreSerializer
    def get_queryset(self, *args, **kwargs):
        return Store.objects.all()


class ListCompaniesApiView(ListAPIView):
    serializer_class = StoreSerializer
    def get_queryset(self, *args, **kwargs):
        companies = Store.objects.filter(fk_store_type=1)
        return companies


class DeliverUserList(ListAPIView):
    
    def get(self, request):
        store = Store.objects.get(fk_user_id=self.request.user.id)
        deliver_users = StoreUser.objects.filter(fk_store_id=store.id)
        abc = []
        for jpt in deliver_users:
            abc.append(jpt.fk_user_id)

        
        users = User.objects.filter(id__in=abc)
        serializer = StoreUserTypeSerializer(users, many=True)
        # print(serializer)
        data = serializer.data[:]
        jzx = {
            "total": users.count(),
            "users": data
        }
        return Response(jzx)
        # user_id_list = []
        # # user_route_id = []
        # for delu in deliver_users:
        #     user_id_list.append(delu.fk_user_id)
        #     # user_route_id
        # data = {}
        # for user in user_id_list:
        #     print(user)
        #     du =  StoreUserTypeSerializer() #User.objects.filter(pk=user).first()

        #     # data = {
        #     # "mobile": du.mobile,
        #     # "email": du.email,

        #     # }
        # #     data.update(data)
        # #     abc = [data]

        # jpt = {
        # "total": 1,
        # "users": du.data
        # }
        # return Response(jpt)

        

        # data = {
        # # "token": self.token,
       
        # "total": deliver_users.count(),
        # "users": del_users.data,
        # # "product_id": items.id,
        # }
        # return Response(data)




