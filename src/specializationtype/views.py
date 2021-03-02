from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from .forms import SpecializationTypeForm
from .models import SpecializationType


# Create your views here.
def index(request):
	specialization_list = SpecializationType.objects.all()
	return render(request, 'specializationtype/index.html', {'specialization_list': specialization_list})


def  add(request):
	if request.method=='POST':
		specialization_details = SpecializationTypeForm(request.POST)

		if specialization_details.is_valid():
			print('Passed')
			specialization_details.save()
			return redirect('/specializationtype', messages.success(request, 'SpecializationType added successfully.', 'alert-success'))
			# return HttpResponse('Added successfully')
		else:
			print(specialization_details.errors)
			print('Failed')
			return redirect('/specializationtype', messages.success(request, 'All fields are required.', 'alert-success'))
	else:
		form = SpecializationTypeForm()
		
	return render(request, 'specializationtype/add.html', {'form':form})




def edit(request, id):
	specialization_details = SpecializationType.objects.get(id=id)

	fstatusType = "Update"
	fpostType = "SpecializationType"
	if request.method=='POST':
		form = SpecializationTypeForm(request.POST, instance=specialization_details)

		if form.is_valid():
			print('Passed')
			if form.save():
				# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Education Info added successfully.', 'alert-success'))
				return redirect('/specializationtype', messages.success(request, 'SpecializationType Management updated successfully', 'alert-success'))
			else:
				return redirect('/specializationtype', messages.success(request, 'There was a problem connecting to the server. Please try again later.', 'alert-success'))
			form.save()
			# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Educations Info added successfully.', 'alert-success'))
	else:
		form = SpecializationTypeForm(instance=specialization_details)

	return render(request, 'specializationtype/add.html', {'form':form, 'fpostType':fpostType})


def delete(request, id):
	print(id)


