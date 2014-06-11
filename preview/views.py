from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from datetime import datetime

from preview.forms import EmailForm
from preview import models as m

# Create your views here.
def preview(request):
	context = {}
	if request.method=='GET':
		form=EmailForm()
		context['form'] = form
	else:
		form=EmailForm(request.POST)
		context['form'] = form
		
		if form.is_valid():
			email=form.cleaned_data['email']
			registered_date=datetime.now()
			emailEntry = m.Email.objects.create(email=email, registered_date=registered_date)
			context['success'] = "Added to mailing list successfully!"
		else:
			context['error'] = "Not a valid email"
	
	return render(request, 'preview/index.html', context)