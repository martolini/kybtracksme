from django.shortcuts import render, redirect
from .models import Workday, Break, Session, Activity
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required


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




