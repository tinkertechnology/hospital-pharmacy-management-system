from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from .forms import NurseForm
from account.models import Account, Nurse


# Create your views here.
def index(request):
	nurse_list = Nurse.objects.all()
	return render(request, 'nurse/index.html', {'nurse_list': nurse_list})


def  add(request):
	fstatusType = "Create"
	fpostType = "Nurse"

	if request.method=='POST':
		nurse_details = NurseForm(request.POST)

		if nurse_details.is_valid():
			print('Passed')
			nurse_details.save()
			return redirect('/nurse', messages.success(request, 'nurse added successfully.', 'alert-success'))
			# return HttpResponse('Added successfully')
		else:
			print(nurse_details.errors)
			print('Failed')
			return redirect('/nurse', messages.success(request, 'All fields are required.', 'alert-success'))
	else:
		form = NurseForm()
		
	return render(request, 'nurse/add.html', {'form':form, 'fstatusType':fstatusType, 'fpostType':fpostType})




def edit(request, id):
	nurse_details = Nurse.objects.get(id=id)

	fstatusType = "Update"
	fpostType = "Nurse Info"
	if request.method=='POST':
		form = NurseForm(request.POST, instance=nurse_details)

		if form.is_valid():
			print('Passed')
			if form.save():
				# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Education Info added successfully.', 'alert-success'))
				return redirect('/nurse', messages.success(request, 'nurse Management updated successfully', 'alert-success'))
			else:
				return redirect('/nurse', messages.success(request, 'There was a problem connecting to the server. Please try again later.', 'alert-success'))
			form.save()
			# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Educations Info added successfully.', 'alert-success'))
	else:
		form = NurseForm(instance=nurse_details)

	return render(request, 'nurse/add.html', {'form':form, 'fpostType':fpostType})


def delete(request, id):
	print(id)


