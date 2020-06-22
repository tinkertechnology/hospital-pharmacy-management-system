from django.shortcuts import render
from .serializers import SliderSerializer
from .models import Slider
from rest_framework import generics

# Create your views here.
class SliderListAPIView(generics.ListAPIView):
	queryset = Slider.objects.all()
	serializer_class = SliderSerializer
	# pagination_class = CategoryPagination