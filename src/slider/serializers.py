from rest_framework import serializers
from django.conf import settings
from .models import Slider



class SliderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Slider
		fields = '__all__'