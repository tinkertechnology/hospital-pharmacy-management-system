from django.shortcuts import render
from .serializers import StateSerializer
# Create your views here.
from .models import State, District, LocalGov
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

class GetSDLdata(ListCreateAPIView):
    serializer_class=StateSerializer
    def get_queryset(self):
        district = self.request.GET.get('district')
        fk_state_id = self.request.GET.get('fk_state_id')
        state = self.request.GET.get('state')
        localgov = self.request.GET.get('localgov')
        fk_district_id = self.request.GET.get('fk_district_id')
        if state:
            return State.objects.all()
        if fk_state_id:
            return District.objects.filter(fk_state_id=fk_state_id)
        if fk_district_id:
            return LocalGov.objects.filter(fk_district_id=fk_district_id)  