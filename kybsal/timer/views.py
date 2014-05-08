from django.shortcuts import render, redirect
from .models import Workday, Break, Session, Activity
from kybsal.slave.models import Slave
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from operator import itemgetter


def frontpage(request):
	activities = Activity.objects.all().order_by('-time')[0:10]
	return render(request, 'index.jade', {'activities': activities})
	
@login_required
def timer_sjekk_in(request):
	w = request.user.workdays.filter(checked_in__day=timezone.now().day)
	if len(w) > 0:
		w = w[0]
		w.active = True
	else:	
		w = Workday(slave=request.user)
	w.save()
	Session(workday=w).save()
	return redirect(reverse('frontpage'))
	
@login_required
def timer_pause(request):
	w = Workday.objects.get(slave=request.user, active=True)
	breaks = w.breaks.filter(active=True).all()
	if len(breaks) > 0:
		b = breaks[0]
		b.active = False
		b.save()
		Session(workday=w).save()
	else:
		s = w.sessions.get(active=True)
		s.active = False
		s.save()
		Break(workday=w).save()
	return redirect(reverse('frontpage'))
	
@login_required
def timer_sjekk_ut(request):
	w = Workday.objects.get(slave=request.user, active=True)
	sessions = w.sessions.filter(active=True).all()
	if len(sessions) > 0:
		s = sessions[0]
		s.active = False
		s.save()
	breaks = w.breaks.filter(active=True).all()
	if len(breaks) > 0:
		b = breaks[0]
		b.active = False
		b.save()
	w.active = False
	w.save()
	return redirect(reverse('frontpage'))

def pause_rom(request):
	breaks = Break.objects.filter(active=True).all()
	slaves = [b.workday.slave for b in breaks]
	return render(request, 'pause.jade', {'slaves': slaves})

def toppliste(request):
	now = timezone.localtime(timezone.now())
	start_of_week = now-timedelta(days=now.weekday())
	weekly_workdays = Workday.objects.filter(date__gte=start_of_week)
	effektiv_data = {}
	pause_data = {}
	total_data = {}
	for workday in weekly_workdays:
		if not workday.slave in effektiv_data:
			effektiv_data[workday.slave] = 0
		if not workday.slave in pause_data:
			pause_data[workday.slave] = 0
		if not workday.slave in total_data:
			total_data[workday.slave] = 0
		effektiv_data[workday.slave] += workday.slave.get_effective_hours_from_workday(workday)
		pause_data[workday.slave] += workday.slave.get_ineffective_hours_from_workday(workday)
		total_data[workday.slave] += workday.slave.get_total_hours_from_workday(workday)
	sorted_effektive_data = sorted(effektiv_data.items(), key=itemgetter(1), reverse=True)
	sorted_pause_data = sorted(pause_data.items(), key=itemgetter(1), reverse=True)
	sorted_total_data = sorted(total_data.items(), key=itemgetter(1), reverse=True)
	effektivtopp = sorted_effektive_data[0:3]
	pausetopp = sorted_pause_data[0:3]
	totaltopp = sorted_total_data[0:3]
	effektivbunn = sorted_total_data[-3:][::-1]
	pausebunn = sorted_pause_data[-3:][::-1]
	totalbunn = sorted_total_data[-3:][::-1]
	return render(request, 'toppliste.jade', {
		'effektivtopp': effektivtopp,
		'effektivbunn': effektivbunn,
		'pausetopp': pausetopp,
		'pausebunn': pausebunn,
		'totaltopp': totaltopp,
		'totalbunn': totalbunn,
		})



