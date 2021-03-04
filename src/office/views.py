from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from .forms import OfficeForm
from .models import Office


# Create your views here.
def index(request):
	office_list = Office.objects.all()
	return render(request, 'office/index.html', {'office_list': office_list})


def  add(request):
	fstatusType = "Add"
	fpostType = "Office"

	if request.method=='POST':
		office_details = OfficeForm(request.POST)

		if office_details.is_valid():
			print('Passed')
			office_details.save()
			return redirect('/office', messages.success(request, 'Office added successfully.', 'alert-success'))
			# return HttpResponse('Added successfully')
		else:
			print(office_details.errors)
			print('Failed')
			return redirect('/office', messages.success(request, 'All fields are required.', 'alert-success'))
	else:
		form = OfficeForm()
	
	return render(request, 'office/add.html', {'form':form, 'fstatusType': fstatusType, 'fpostType': fpostType})




def edit(request, id):
	office_details = Office.objects.get(id=id)

	fstatusType = "Update"
	fpostType = "Office"
	if request.method=='POST':
		form = OfficeForm(request.POST, request.FILES, instance=office_details)

		if form.is_valid():
			print('Passed')
			if form.save():
				# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Education Info added successfully.', 'alert-success'))
				return redirect('/office', messages.success(request, 'Office Management updated successfully', 'alert-success'))
			else:
				return redirect('/office', messages.success(request, 'There was a problem connecting to the server. Please try again later.', 'alert-success'))
			form.save()
			# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Educations Info added successfully.', 'alert-success'))
	else:
		form = OfficeForm(instance=office_details)

	return render(request, 'office/add.html', {'form':form, 'fpostType':fpostType})


def delete(request, id):
	print(id)


