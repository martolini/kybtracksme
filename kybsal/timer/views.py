from django.shortcuts import render, redirect
from .models import Workday, Break, Session, Activity, FeedItem, Action
from .forms import CreateFeedItemForm
from kybsal.slave.models import Slave
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from operator import itemgetter

def vedlikehold(request):
	return render(request, 'vedlikehold.jade')

def frontpage(request):
	feed = FeedItem.objects.all().order_by('-created')[0:10]
	return render(request, 'index.jade', {'feed': feed})
	
@login_required
def timer_sjekk_in(request):
	current_session = request.user.get_current_action()
	if not current_session:
		FeedItem(slave=request.user, desc="%s sjekket inn!" % request.user.get_full_name()).save()
		request.user.create_session()
	return redirect(reverse('frontpage'))
	
@login_required
def timer_pause(request):
	current_action = request.user.get_current_action()
	if current_action:
		current_action.end()
		if current_action.is_break():
			desc = "er ferdig med pausa!"
			request.user.create_session()
		elif current_action.is_session():
			desc = "tok en pause!"
			request.user.create_break()
		else:
			return redirect(reverse('frontpage'))
		FeedItem(slave=request.user, desc="%s %s" % (request.user.get_full_name(), desc)).save()
	return redirect(reverse('frontpage'))
	
@login_required
def timer_sjekk_ut(request):
	current_action = request.user.get_current_action()
	if current_action:
		current_action.end()
		FeedItem(slave=request.user, desc="%s sjekket ut!" % request.user.get_full_name()).save()
	return redirect(reverse('frontpage'))

def pause_rom(request):
	slaves = [a.slave for a in Action.objects.filter(action="BREAK", ended=None)]
	return render(request, 'pause.jade', {'slaves': slaves})

def toppliste(request):
	now = timezone.localtime(timezone.now())
	start_of_week = now-timedelta(days=now.weekday(), hours=now.hour)
	effektiv_data, pause_data, total_data = {}, {}, {}
	for slave in Slave.objects.all().exclude(pk=1):
		data = {'effektiv': 0, 'pause': 0}
		actions = slave.actions.filter(started__gte=start_of_week)
		effektiv_data[slave] = slave.get_effective_hours(actions)
		pause_data[slave] = slave.get_ineffective_hours(actions)
		total_data[slave] = slave.get_total_hours(actions)

	sorted_effektiv_data = sorted(effektiv_data.items(), key=itemgetter(1), reverse=True)
	sorted_pause_data = sorted(pause_data.items(), key=itemgetter(1), reverse=True)
	sorted_total_data = sorted(total_data.items(), key=itemgetter(1), reverse=True)
	effektivtopp = sorted_effektiv_data[0:10]
	pausetopp = sorted_pause_data[0:10]
	totaltopp = sorted_total_data[0:10]

	effektivbunn = sorted_effektiv_data[-10:][::-1]
	pausebunn = sorted_pause_data[-10:][::-1]
	totalbunn = sorted_total_data[-10:][::-1]
	return render(request, 'toppliste.jade', {
		'effektivtopp': effektivtopp,
		'effektivbunn': effektivbunn,
		'pausetopp': pausetopp,
		'pausebunn': pausebunn,
		'totaltopp': totaltopp,
		'totalbunn': totalbunn,
		})

@login_required
def post_feed(request):
	if request.POST:
		form = CreateFeedItemForm(request.POST)
		if form.is_valid():
			form.save(request.user)
		else:
			print form.errors
	return redirect(reverse('frontpage'))



