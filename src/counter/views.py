from django.shortcuts import render, redirect, get_object_or_404
from .models import Counter
from .forms import CounterForm
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.
def index(request):
	counter_list = Counter.objects.all()
	return render(request, 'counter/index.html', {'counter_list': counter_list})


def  add(request):
	fstatusType = "Create New"
	fpostType = "Counter"

	if request.method == 'POST':
		form = CounterForm(request.POST)
		if form.is_valid():
			print('Passed')  # does nothing, just trigger the validation
			form.save()
			# return HttpResponse('Counter added successfully')
			messages.success(request, 'Counter details added successfully!') 
			return redirect('/counter')
		else:
			form = CounterForm(request.POST)
			messages.warning(request, 'Please correct the error below.')
	else:
		form = CounterForm()
	return render(request, 'counter/add.html', {'form': form, 'fstatusType':fstatusType, 'fpostType':fpostType})




def edit(request, id):
	counter_details = Counter.objects.get(id=id)

	fstatusType = "Update"
	fpostType = "Counter"
	if request.method=='POST':
		form = CounterForm(request.POST, request.FILES, instance=counter_details)

		if form.is_valid():
			print('Passed')
			if form.save():
				return redirect('/counter', messages.success(request, 'Counter Management updated successfully', 'alert-success'))
			else:
				form = CounterForm(instance=counter_details)
				messages.warning(request, 'Please correct the error below.')
				# return redirect('/counter', messages.success(request, 'There was a problem connecting to the server. Please try again later.', 'alert-success'))
			form.save()
	else:
		form = CounterForm(instance=counter_details)

	return render(request, 'counter/add.html', {'form':form, 'fpostType':fpostType})


def delete(request, id):
	counter_details = Counter.objects.filter(id=id).delete()
	messages.success(request, 'Counter details deleted Successfully.')
	return redirect('/counter')

