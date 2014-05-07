from django.db import models
from django.contrib.auth.models import AbstractUser
from kybsal.timer.models import Workday, Session, Break
from datetime import datetime


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

	def get_active_break(self):
		breaks = Break.objects.filter(workday__slave=self, active=True)
		if len(breaks) > 0:
			return breaks[0]
		return None

	def get_todays_effective_hours(self):
		workday = self.workdays.filter(active=True)
		if len(workday) == 0:
			return 0
		workday = workday[0]
		active_session = workday.sessions.filter(active=True)
		if len(active_session) > 0:
			s = active_session[0]
			s.save()
		return sum([round((session.ended-session.started).seconds/3600.0,1) for session in workday.sessions.all()])

	def get_todays_total_hours(self):
		workday = self.workdays.filter(active=True)
		if len(workday) == 0:
			return 0
		workday = workday[0]
		workday.save()
		return round((workday.checked_out-workday.checked_in).seconds/3600.0,1)

	def get_total_hours(self):
		active_workday = self.workdays.filter(active=True)
		if len(active_workday) > 0:
			active_workday[0].save()
		return sum([round((workday.checked_out-workday.checked_in).seconds/3600.0,1) for workday in self.workdays.all()])