from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
# from .import models

class BuyDrinkingWaterForm(forms.Form):
	select_location = forms.CharField(max_length=200, widget=forms.Select(attrs={'class':'form-control'}))
	full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	phone = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	select_depot = forms.CharField(max_length=200, widget=forms.Select(attrs={'class':'form-control'}))
	select_brand = forms.CharField(max_length=200, widget=forms.Select(attrs={'class':'form-control'}))
	select_purchase_type = forms.CharField(max_length=200, widget=forms.Select(attrs={'class':'form-control'}))


class OpenDepotForm(forms.Form):
	full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	phone = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	location = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	message = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))


class FeedbackForm(forms.Form):
	full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	phone = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	message = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))


class ComplaintForm(forms.Form):
	full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	phone = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	select_location = forms.CharField(max_length=200, widget=forms.Select(attrs={'class':'form-control'}))
	message = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))

class VacancyForm(forms.Form):
	full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	phone = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	cv = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))
	citizenship = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))

	class Meta:
		fields = ['full_name', 'phone', 'email', 'address', 'cv', 'citizenship']

# def file_size(value): 
# 	limit = 2 * 1024 * 1024
# 	if value.size > limit:
# 		raise ValidationError('File too large. Size should not exceed 2 MiB.')



	def clean_fullname(self):
		full_name = self.cleaned_data['full_name']
		if len(full_name)<3:
			raise forms.ValidationError('Username is too short')
		return full_name