from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()



# Create your models here.
class Route(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    code = models.CharField(max_length=500, null=True, blank=True)

    #route.fk_store ahile cha
    fk_store = models.ForeignKey("store.Store", related_name='fk_store_route', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
    	return self.title

class RouteDetail(models.Model):
    fk_route = models.ForeignKey(Route, related_name='fk_route_route_detail', on_delete=models.CASCADE, null=False, blank=False)

    order_latitude = models.CharField(max_length=200, null=True, blank=True)
    order_longitude = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
    	return self.fk_route


def get_nearyby_routes(latitude, longitude, store_id=None, max_distance=None):
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
    qs = RouteDetail.objects.all() \
    .annotate(distance=distance_raw_sql)\
    .order_by('distance')
    if max_distance is not None:
        qs = qs.filter( distance__lt= float(max_distance) )
    if store_id is not None:
        qs = qs.filter( fk_store_id = int(store_id))

    print(qs.query)
    print(qs.all())
    return qs

def get_nearest_route(lat,lng,store_id=None, max_dis=None):
    qs_route_details = get_nearyby_routes(lat, lng, store_id, max_dis)
    route_details = qs_route_details.first()
    if route_details is None:
        return None
    return route_details.fk_route
    