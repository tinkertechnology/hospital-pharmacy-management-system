from rest_framework import serializers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Route, RouteDetail


class RouteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Route
		fields= '__all__'

class RouteDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = RouteDetail
		fields= '__all__'