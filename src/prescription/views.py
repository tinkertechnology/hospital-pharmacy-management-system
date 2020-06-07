
from .serializer import FileUploaderSerializer, FileSerializer
from rest_framework import generics
from .models import Prescription
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
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


from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

class MyUploadView(generics.ListCreateAPIView):
	parser_class = (FileUploadParser,)
	# serializer = FileSerializer(data=request.data)
	# serializer_class = FileUploaderSerializer

	def put(self, request, format=None):
		serializer_class = FileSerializer(data=self.request.data)
		# serializer_class = FileUploaderSerializer
		print('jpt')
		if 'photo' not in request.data:
			raise ParseError("Empty content")

		f = request.data['photo']

		Prescription.file.save(f.name, f, save=True)
		return Response(status=status.HTTP_201_CREATED)

# views.py
# from rest_framework.views import APIView
# class FileUploadView(requ):
# 	parser_classes = [FileUploadParser]

# 	def put(self, request, filename, format=None):
# 		file_obj = request.data['file']
# # ...
# # do some stuff with uploaded file
# # ...
# 		return Response(status=204)


from django.http import HttpResponseRedirect
from django.shortcuts import render
# from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required


@csrf_exempt
@login_required
def upload_file(request):
	if request.method == 'POST':
		print(request.FILES)

        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():

		instance = Prescription(file=request.FILES['file'])
		instance.user_id = request.user.id
		print(request.user.id)
		instance.save()
            # instance.save()
		return HttpResponseRedirect('/success/url/')
	else:
        # form = UploadFileForm()

		print('jpt')
	return render(request, 'upload.html', {'form': form})

class ApiPostFile(APIView):

	def  post(self, request, *args, **kwargs):
		print(request.FILES)
		instance = Prescription(file=request.FILES['file'])
		instance.user_id = request.user.id
		print(request.user.id)
		instance.save()
		return Response({
							'status': True,
							'detail': 'OTP sent to '
							})