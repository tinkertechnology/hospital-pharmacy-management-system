from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib import messages
from io import BytesIO
import mimetypes
import smtplib

from counter.models import Counter
from .forms import * 

def index(request):
	page_title = 'Home'
	lang = request.GET.get('lang')
	counters = Counter.objects.all()
	if request.user.is_authenticated:
		return redirect('/dashboard/')
	return render(request, 'hms/index.html', {'title_content':page_title, 'lang':lang, 'counters': counters})
	# return HttpResponse('index page')



def handler404(request, exception):
    # return HttpResponse('404 Page Error')
    return render(request, 'hms/404.html')


def handler500(request, exception=None):
    # return HttpResponse('404 Page Error')
    return render(request, 'hms/500.html')