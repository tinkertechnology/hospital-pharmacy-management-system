from django.shortcuts import render
from rest_framework import serializers
from .models import Prescription
from rest_framework import viewsets
# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()

class FileUploaderSerializer(serializers.ModelSerializer):
    # overwrite = serializers.BooleanField()
    class Meta:
        model = Prescription
        fields = ('file','name','version','upload_date', 'size')
        read_only_fields = ('name','version','user','upload_date', 'size')

    def validate(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['name'] = os.path.splitext(validated_data['file'].name)[0]
        validated_data['size'] = validated_data['file'].size
        #other validation logic
        return validated_data

    def create(self, validated_data):
        return Prescription.objects.create(**validated_data)

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()