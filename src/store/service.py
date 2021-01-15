from django.shortcuts import render
from .serializers import StoreSerializer
from .models import Store, StoreAccount, StoreUser
from django.conf import settings	
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

#https://stackoverflow.com/questions/19703975/django-sort-by-distance
from django.db import models
from django.db.models.expressions import RawSQL
from django.db.models.functions import Greatest
from decimal import Decimal
def UserAccountStoreWiseSaveService(data):
	fk_user_id = data.get('fk_user_id')
	fk_store_id = data.get('fk_store_id')
	credit = data.get('credit', 0.0)
	print('00000')
	print(credit)
	cart_query = StoreAccount.objects.filter(fk_user_id=fk_user_id).filter(fk_store_id=fk_store_id)
	cart = cart_query.first()

	if cart == None:
		dict_cart = {}
		cart = StoreAccount.objects.create(fk_user_id=fk_user_id, **dict_cart)
		# cart.fk_user_id = fk_user_id
		cart.fk_store_id = fk_store_id
		cart.credit=0
	cart.credit += Decimal(credit)
	# if cart.credit < 0: #dherai +cash ayo bhane - ma credit nabasos
 		# cart.credit = 0
	cart.save()
	return cart
    

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



def getUserStoreService(user_id):
    settings.DLFPRINT()
    # queryset = Product.objects.all() ##debug if not working location
    # return queryset
    users_store = None #user ko store (instance of Store)
    main_users_store = Store.objects.filter(fk_user_id=user_id).first() #company / depo ko main user #(instance Store)

    #todo: make service for getting store of user, isUserStore, isUserCustomer
    if main_users_store is not None:
        users_store = main_users_store
    else:
        storeUser = StoreUser.objects.filter(fk_user_id=user_id).first()
        if(storeUser is not None):
            users_store = storeUser.fk_store
    return users_store
    