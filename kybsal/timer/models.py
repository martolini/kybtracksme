from django.db import models
from string import capwords

class Workday(models.Model):
	slave = models.ForeignKey('slave.Slave', related_name="workdays")
	date = models.DateField(auto_now_add=True)
	checked_in = models.DateTimeField(auto_now_add=True)
	checked_out = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

class Break(models.Model):
	started = models.DateTimeField(auto_now_add=True)
	ended = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	workday = models.ForeignKey(Workday, related_name="breaks")

	def save(self, *args, **kwargs):
		super(Break, self).save(*args, **kwargs)
		if self.active:
			desc = "%s tok en pause!" % capwords(self.workday.slave.get_full_name())
		else:
			desc = "%s er ferdig med pausa!" % capwords(self.workday.slave.get_full_name())
		Activity(desc=desc, workday=self.workday).save()


class Session(models.Model):
	started = models.DateTimeField(auto_now_add=True)
	ended = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	workday = models.ForeignKey(Workday, related_name="sessions")

class Activity(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	desc = models.CharField(max_length=100)
	workday = models.ForeignKey(Workday, related_name='activities')
