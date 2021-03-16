from rest_framework.response import Response
from rest_framework import serializers
from .models import State, District, LocalGov

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class LocalGovernmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalGov
        fields = '__all__'   