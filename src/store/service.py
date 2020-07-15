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

def get_qs_store_locations_nearby_coords(latitude, longitude, max_distance=None,fk_store_type_id=None):
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

    if fk_store_type_id is not None:
        qs = qs.filter( fk_store_type_id=fk_store_type_id )

    qs = qs.exclude(latitude__isnull=True).exclude(longitude__isnull=True)


    print(qs.query)
    print(qs.all())
    return qs