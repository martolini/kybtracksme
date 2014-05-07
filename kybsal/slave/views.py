from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SlaveCreationForm
from .models import Slave
from kybsal.timer.models import Activity
from django.core.urlresolvers import reverse
from kybsal.timer.views import timer_sjekk_ut
from django.db.models import Q

def login_view(request):
	if request.POST:
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			auth.login(request, form.get_user())
	return redirect(reverse('frontpage'))

def signup_view(request):
	if request.POST:
		form = SlaveCreationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password2']
			form.save()
			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)
		else:
			messages.warning(request, "Fyll inn formet riktig!")
	return redirect(reverse('frontpage'))

def search_view(request):
	if request.POST:
		query = request.POST.get('query')
		slaves = Slave.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)).exclude(username='admin')
		return render(request, 'search.jade', {'slaves': slaves})
	return redirect(reverse('frontpage'))
	
@login_required
def logout_view(request):
	timer_sjekk_ut(request)
	auth.logout(request)
	return redirect(reverse('frontpage'))

def profile_view(request, username=False):
	if username == 'admin':
		return redirect(reverse('frontpage'))
	slave = get_object_or_404(Slave, username=username)
	activities = Activity.objects.filter(workday__slave=slave).order_by('-time')[0:10]
	return render(request, 'slave.jade', {'slave': slave, 'activities': activities})

