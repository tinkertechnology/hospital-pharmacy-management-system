from django.shortcuts import render
from .models import Counter
from .forms import CounterForm

# Create your views here.
def index(request):
	counter_list = Counter.objects.all()
	return render(request, 'counter/index.html', {'counter_list': counter_list})


def  add(request):
	fstatusType = "Add"
	fpostType = "Counter"

	if request.method=='POST':
		counter_details = CounterForm(request.POST)

		if counter_details.is_valid():
			print('Passed')
			counter_details.save()
			return redirect('/counter', messages.success(request, 'Counter added successfully.', 'alert-success'))
			# return HttpResponse('Added successfully')
		else:
			print(counter_details.errors)
			print('Failed')
			return redirect('counter', messages.success(request, 'All fields are required.', 'alert-success'))
	else:
		form = CounterForm()
	
	return render(request, 'counter/add.html', {'form':form, 'fstatusType': fstatusType, 'fpostType': fpostType})




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
				return redirect('/counter', messages.success(request, 'There was a problem connecting to the server. Please try again later.', 'alert-success'))
			form.save()
	else:
		form = CounterForm(instance=counter_details)

	return render(request, 'counter/add.html', {'form':form, 'fpostType':fpostType})


def delete(request, id):
	print(id)
