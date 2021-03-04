from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from .forms import VendorForm
from .models import Vendor


# Create your views here.
def index(request):
	vendor_list = Vendor.objects.all()
	return render(request, 'vendor/index.html', {'vendor_list': vendor_list})


def  add(request):
	fstatusType = "Add"
	fpostType = "Vendor"

	if request.method=='POST':
		vendor_details = VendorForm(request.POST)

		if vendor_details.is_valid():
			print('Passed')
			vendor_details.save()
			return redirect('/vendor', messages.success(request, 'Vendor added successfully.', 'alert-success'))
			# return HttpResponse('Added successfully')
		else:
			print(vendor_details.errors)
			print('Failed')
			return redirect('vendor', messages.success(request, 'All fields are required.', 'alert-success'))
	else:
		form = VendorForm()
	
	return render(request, 'vendor/add.html', {'form':form, 'fstatusType': fstatusType, 'fpostType': fpostType})




def edit(request, id):
	vendor_details = Vendor.objects.get(id=id)

	fstatusType = "Update"
	fpostType = "Vendor"
	if request.method=='POST':
		form = VendorForm(request.POST, request.FILES, instance=vendor_details)

		if form.is_valid():
			print('Passed')
			if form.save():
				# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Education Info added successfully.', 'alert-success'))
				return redirect('/vendor', messages.success(request, 'Vendor Management updated successfully', 'alert-success'))
			else:
				return redirect('/vendor', messages.success(request, 'There was a problem connecting to the server. Please try again later.', 'alert-success'))
			form.save()
			# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Educations Info added successfully.', 'alert-success'))
	else:
		form = VendorForm(instance=vendor_details)

	return render(request, 'vendor/add.html', {'form':form, 'fpostType':fpostType})


def delete(request, id):
	print(id)


