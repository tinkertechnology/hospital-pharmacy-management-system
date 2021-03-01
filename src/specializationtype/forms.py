from django import forms
from django.forms import ModelForm
from .models import SpecializationType

class SpecializationTypeForm(ModelForm):
	name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)

	class Meta:
		model = SpecializationType
		fields = '__all__'


