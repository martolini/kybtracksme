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
from datetime import datetime, timedelta
from django.utils import timezone


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
	if request.user.get_active_workday():
		timer_sjekk_ut(request)
	auth.logout(request)
	return redirect(reverse('frontpage'))


def profile_view(request, pk=None):
	if not pk or pk == 1:
		return redirect(reverse('frontpage'))
	slave = get_object_or_404(Slave, pk=pk)
	activities = Activity.objects.filter(workday__slave=slave).order_by('-time')[0:10]
	since = timezone.now()-timedelta(days=7)
	data = {}
	for date in range(8):
		data[since.strftime("%Y-%m-%d")] = {'effektive_timer': 0, 'ineffektive_timer': 0, 'totale_timer': 0}
		since += timedelta(days=1)
	since = timezone.now()-timedelta(days=7)
	workdays = slave.workdays.filter(checked_in__gte=since)
	for workday in workdays:
		key = workday.date.strftime("%Y-%m-%d")
		data[key]['effektive_timer'] = slave.get_effective_hours_from_workday(workday)
		data[key]['ineffektive_timer'] = slave.get_ineffective_hours_from_workday(workday)
		data[key]['totale_timer'] = data[key]['effektive_timer'] + data[key]['ineffektive_timer']

	workday = slave.get_today_workday()
	effektive_timer = slave.get_effective_hours_from_workday(workday)
	totale_timer_idag = slave.get_total_hours_from_workday(workday)
	totale_timer = slave.get_total_hours()

	return render(request, 'slave.jade', {
		'slave': slave, 
		'activities': activities, 
		'data': data,
		'effektive_timer': effektive_timer,
		'totale_timer_idag': totale_timer_idag,
		'totale_timer': totale_timer
		})

def status(request):
	slaves = sorted(Slave.objects.all().exclude(pk=1), key=lambda x:x.get_current_state(), reverse=True)
	return render(request, 'status.jade', {'slaves': slaves})

