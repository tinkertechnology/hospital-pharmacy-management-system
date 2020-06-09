
from .serializer import FileUploaderSerializer, FileSerializer
from rest_framework import generics
from .models import Prescription
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import permissions
# from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
User = get_user_model()

class FileUploaderViewSet(viewsets.ModelViewSet):
    serializer_class = FileUploaderSerializer
    parser_classes = (MultiPartParser, FormParser,)

    # overriding default query set
    queryset = Prescription.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = super(FileUploaderViewSet, self).get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs






class ApiPostFile(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def  post(self, request, *args, **kwargs):
		print(request.FILES)
		print(request.POST)
		instance = Prescription(file=request.FILES['file'])
		instance.user_id = request.user.id
		instance.doctor_name = request.POST.get('doctor_name')
		instance.hospital_name = request.POST.get('hospital_name')
		instance.save()
		return Response({
			'status': True,
			'detail': 'Saved Prescription'
			})

