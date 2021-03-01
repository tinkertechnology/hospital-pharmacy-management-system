from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from .forms import DoctorForm
from account.models import Account, Doctor


# Create your views here.
def index(request):
	doctor_list = Doctor.objects.all()
	return render(request, 'doctor/index.html', {'doctor_list': doctor_list})


def  add(request):
	fstatusType = "Create"
	fpostType = "Doctor"

	if request.method=='POST':
		doctor_details = DoctorForm(request.POST)

		if doctor_details.is_valid():
			print('Passed')
			doctor_details.save()
			return redirect('/doctor', messages.success(request, 'Doctor added successfully.', 'alert-success'))
			# return HttpResponse('Added successfully')
		else:
			print(doctor_details.errors)
			print('Failed')
			return redirect('/doctor', messages.success(request, 'All fields are required.', 'alert-success'))
	else:
		form = DoctorForm()
		
	return render(request, 'doctor/add.html', {'form':form, 'fstatusType':fstatusType, 'fpostType':fpostType})




def edit(request, id):
	doctor_details = Doctor.objects.get(id=id)

	fstatusType = "Update"
	fpostType = "Doctor Info"
	if request.method=='POST':
		form = DoctorForm(request.POST, instance=doctor_details)

		if form.is_valid():
			print('Passed')
			if form.save():
				# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Education Info added successfully.', 'alert-success'))
				return redirect('/doctor', messages.success(request, 'Doctor Management updated successfully', 'alert-success'))
			else:
				return redirect('/doctor', messages.success(request, 'There was a problem connecting to the server. Please try again later.', 'alert-success'))
			form.save()
			# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Educations Info added successfully.', 'alert-success'))
	else:
		form = DoctorForm(instance=doctor_details)

	return render(request, 'doctor/add.html', {'form':form, 'fpostType':fpostType})


def delete(request, id):
	print(id)


