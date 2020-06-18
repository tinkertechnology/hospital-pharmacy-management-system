from django.shortcuts import render
from .serializers import StoreSerializer
from .models import Store

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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