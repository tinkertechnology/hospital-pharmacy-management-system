from django import forms
from django.forms import ModelForm

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