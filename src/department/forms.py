from django import forms
from django.forms import ModelForm
from .models import Department

class DepartmentForm(ModelForm):
	name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)

	class Meta:
		model = Department
		fields = '__all__'


