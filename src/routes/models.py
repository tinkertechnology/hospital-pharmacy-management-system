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