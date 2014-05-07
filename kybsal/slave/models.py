from django.db import models
from django.contrib.auth.models import AbstractUser
from kybsal.timer.models import Workday, Session, Break
from datetime import datetime
from itertools import chain



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

	def get_todays_effective_hours(self):
		workday = self.get_active_workday()
		if not workday:
			return None
		return sum([round((session.ended-session.started).seconds/3600.0,1) for session in workday.sessions.all()])

	def get_todays_total_hours(self):
		workday = self.get_active_workday()
		if not workday:
			return None
		sessions, breaks = workday.sessions.all(), workday.breaks.all()
		alle = chain(sessions, breaks)
		return sum([round((s.ended-s.started).seconds/3600.0,1) for s in alle])

	def get_total_hours(self):
		workdays = self.workdays.all()
		total = 0
		for workday in workdays:
			alle = chain(workday.sessions.all(), workday.breaks.all())
			total += sum([round((s.ended-s.started).seconds/3600.0,1) for s in alle])
		return total

