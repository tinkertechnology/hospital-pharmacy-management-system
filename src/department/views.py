from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from .forms import DepartmentForm
from .models import Department


# Create your views here.
def index(request):
	department_list = Department.objects.all()
	return render(request, 'department/index.html', {'department_list': department_list})


def  add(request):
	if request.method=='POST':
		department_details = DepartmentForm(request.POST)

		if department_details.is_valid():
			print('Passed')
			department_details.save()
			return redirect('/department', messages.success(request, 'department added successfully.', 'alert-success'))
			# return HttpResponse('Added successfully')
		else:
			print(department_details.errors)
			print('Failed')
			return redirect('/department', messages.success(request, 'All fields are required.', 'alert-success'))
	else:
		form = DepartmentForm()
		
	return render(request, 'department/add.html', {'form':form})




def edit(request, id):
	department_details = Department.objects.get(id=id)

	fstatusType = "Update"
	fpostType = "department"
	if request.method=='POST':
		form = DepartmentForm(request.POST, request.FILES, instance=department_details)

		if form.is_valid():
			print('Passed')
			if form.save():
				# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Education Info added successfully.', 'alert-success'))
				return redirect('/department', messages.success(request, 'department Management updated successfully', 'alert-success'))
			else:
				return redirect('/department', messages.success(request, 'There was a problem connecting to the server. Please try again later.', 'alert-success'))
			form.save()
			# return redirect('/employee/%s/edit' %(emp_id), messages.success(request, 'Educations Info added successfully.', 'alert-success'))
	else:
		form = DepartmentForm(instance=department_details)

	return render(request, 'department/add.html', {'form':form, 'fpostType':fpostType})


def delete(request, id):
	print(id)


