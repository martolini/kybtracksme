from django.db import models
from django.contrib.auth.models import AbstractUser
from kybsal.timer.models import Workday, Session, Break
from datetime import date
from itertools import chain
from django.utils import timezone



class Slave(AbstractUser):
	def get_current_state(self):
		w = Workday.objects.filter(slave=self, active=True).all()
		if len(w) > 0:
			w = w[0]
			breaks = w.breaks.filter(workday=w, active=True).all()
			if len(breaks) > 0:
				return 2
			else:
				return 1
		return 0

	def get_active_workday(self):
		workday = self.workdays.filter(active=True)
		if len(workday) == 0:
			return None
		return workday[0]

	def get_today_workday(self):
		workday = self.workdays.filter(date=date.today())
		if not workday:
			return None
		return workday[0]

	def get_active_break(self):
		breaks = Break.objects.filter(workday__slave=self, active=True)
		if len(breaks) > 0:
			return breaks[0]
		return None

	def get_active_session(self):
		sessions = Session.objects.filter(workday__slave=self, active=True)
		if len(sessions) > 0:
			return sessions[0]
		return None

	def get_effective_hours_from_workday(self, workday):
		if not workday:
			return 0
		session = self.get_active_session()
		hours = 0
		if session:
			hours = (timezone.now()-session.started).seconds/3600.0
		return round(sum([(session.ended-session.started).seconds/3600.0 for session in workday.sessions.filter(active=False)])+hours,1)

	def get_ineffective_hours_from_workday(self, workday):
		if not workday:
			return 0
		b = self.get_active_break()
		hours = 0
		if b:
			hours = (timezone.now()-b.started).seconds/3600.0
		return round(sum([(b.ended-b.started).seconds/3600.0 for b in workday.breaks.filter(active=False)])+hours,1)

	def get_total_hours_from_workday(self, workday):
		if not workday:
			return 0
		now = timezone.now()
		session = self.get_active_session()
		hours = 0
		if session:
			hours += (now-session.started).seconds/3600.0
		b = self.get_active_break()
		if b:
			hours += (now-b.started).seconds/3600.0
		sessions, breaks = workday.sessions.filter(active=False), workday.breaks.filter(active=False)
		alle = chain(sessions, breaks)
		return round(sum([(s.ended-s.started).seconds/3600.0 for s in alle])+hours,1)

	def get_total_hours(self):
		workdays = self.workdays.all()
		total = 0
		now = timezone.now()
		session = self.get_active_session()
		if session:
			total += (now-session.started).seconds/3600.0
		b = self.get_active_break()
		if b:
			total += (now-b.started).seconds/3600.0
		for workday in workdays:
			alle = chain(workday.sessions.all(), workday.breaks.all())
			total += sum([(s.ended-s.started).seconds/3600.0 for s in alle])
		return round(total,1)

