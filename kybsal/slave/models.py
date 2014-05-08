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
		return round(sum([(session.ended-session.started).seconds/3600.0 for session in workday.sessions.all()]),1)

	def get_ineffective_hours_from_workday(self, workday):
		if not workday:
			return 0
		return round(sum([(b.ended-b.started).seconds/3600.0 for b in workday.breaks.all()]),1)

	def get_total_hours_from_workday(self, workday):
		if not workday:
			return 0
		sessions, breaks = workday.sessions.all(), workday.breaks.all()
		alle = chain(sessions, breaks)
		return round(sum([(s.ended-s.started).seconds/3600.0 for s in alle]),1)

	def get_total_hours(self):
		workdays = self.workdays.all()
		total = 0
		for workday in workdays:
			alle = chain(workday.sessions.all(), workday.breaks.all())
			total += round(sum([(s.ended-s.started).seconds/3600.0 for s in alle]),1)
		return total

