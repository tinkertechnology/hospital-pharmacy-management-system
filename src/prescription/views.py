
from .serializer import FileUploaderSerializer
from .models import Prescription
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
class FileUploaderViewSet(viewsets.ModelViewSet):
    serializer_class = FileUploaderSerializer
    parser_classes = (MultiPartParser, FormParser,)

    # overriding default query set
    queryset = Prescription.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = super(FileUploaderViewSet, self).get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs