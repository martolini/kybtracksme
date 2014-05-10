from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SlaveCreationForm
from .models import Slave
from kybsal.timer.models import Activity, FeedItem
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
	current_action = request.user.get_current_action()
	if current_action:
		current_action.end()
	auth.logout(request)
	return redirect(reverse('frontpage'))


def profile_view(request, pk=None):
	slave = get_object_or_404(Slave, pk=pk)
	feed = FeedItem.objects.filter(slave=slave).order_by('-created')[0:10]
	data = {}
	now = timezone.localtime(timezone.now())
	since = timezone.localtime(timezone.now())-timedelta(days=7)
	for date in range(7):
		key = since.strftime("%Y-%m-%d")
		data[key] = {}
		start = since-timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
		end = since+timedelta(hours=23-now.hour, minutes=59-now.minute, seconds=59-now.second)
		r = [start, end]
		data[key]['effektive_timer'] = slave.get_effective_hours(slave.actions.filter(started__range=r))
		data[key]['ineffektive_timer'] = slave.get_ineffective_hours(slave.actions.filter(started__range=r))
		data[key]['totale_timer'] = slave.get_total_hours(slave.actions.filter(started__range=r))
		since += timedelta(days=1)
	key = since.strftime("%Y-%m-%d")
	start = since-timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
	end = since+timedelta(hours=23-now.hour, minutes=59-now.minute, seconds=59-now.second)
	r = [start, end]
	data[key] = {}
	data[key]['effektive_timer'] = slave.get_effective_hours(slave.actions.filter(started__range=r))
	data[key]['ineffektive_timer'] = slave.get_ineffective_hours(slave.actions.filter(started__range=r))
	data[key]['totale_timer'] = slave.get_total_hours(slave.actions.filter(started__range=r))

	return render(request, 'slave.jade', {
		'slave': slave, 
		'feed': feed, 
		'data': data,
		'effektive_timer': data[key]['effektive_timer'],
		'totale_timer_idag': data[key]['ineffektive_timer'],
		'totale_timer': data[key]['totale_timer']
		})

def status(request):
	slaves = sorted(Slave.objects.all(), key=lambda x:x.get_current_state(), reverse=True)
	return render(request, 'status.jade', {'slaves': slaves})

