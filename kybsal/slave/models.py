from django.db import models
from django.contrib.auth.models import AbstractUser
from kybsal.timer.models import Workday, Session, Break, Action
from datetime import datetime
from itertools import chain
from django.utils import timezone

class Slave(AbstractUser):
	def get_current_state(self):
		action = self.get_current_action()
		if not action:
			return 0
		if action.is_session():
			return 1
		if action.is_break():
			return 2
		return 0

	def create_session(self):
		return Action.objects.create(slave=self, action="SESSION")

	def create_break(self):
		return Action.objects.create(slave=self, action="BREAK")

	def get_current_action(self):
		actions = self.actions.filter(ended=None)
		if len(actions) > 0:
			return actions[0]
		return None

	def get_effective_hours(self, queryset):
		return self.get_total_hours(queryset.filter(action="SESSION"))

	def get_ineffective_hours(self, queryset):
		return self.get_total_hours(queryset.filter(action="BREAK"))


	def get_total_hours(self, queryset):
		timer = 0
		for action in queryset:
			if not action.ended:
				ended = timezone.localtime(timezone.now())
			else:
				ended = action.ended
			started = action.started
			timer += (ended-started).seconds/3600.0
		return round(timer,1)

