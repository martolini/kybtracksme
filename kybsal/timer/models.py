from django.db import models
from string import capwords
from django.utils import timezone

class TodayManager(models.Manager):
	use_for_related_fields = True
	def get_queryset(self):
		today = timezone.localtime(timezone.now()).date
		return super(TodayManager, self).get_queryset().filter(started__gte=today)

class Workday(models.Model):
	slave = models.ForeignKey('slave.Slave', related_name="workdays")
	date = models.DateField(auto_now_add=True)
	checked_in = models.DateTimeField(auto_now_add=True)
	checked_out = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		super(Workday, self).save(*args, **kwargs)
		if self.active:
			desc = "%s sjekket inn!" % capwords(self.slave.get_full_name())
		else:
			desc = "%s sjekket ut!" % capwords(self.slave.get_full_name())
		Activity(desc=desc, workday=self).save()


	def __unicode__(self):
		return unicode(self.date)

class Break(models.Model):
	started = models.DateTimeField(auto_now_add=True)
	ended = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	workday = models.ForeignKey(Workday, related_name="breaks")
	slave = models.ForeignKey('slave.Slave', related_name='breaks', blank=True, null=True)

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
	slave = models.ForeignKey('slave.Slave', related_name='sessions', blank=True, null=True)

class Activity(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	desc = models.CharField(max_length=100)
	workday = models.ForeignKey(Workday, related_name='activities')

class Action(models.Model):
	ACTION_CHOICES = (
		("BREAK", "Pause"),
		("SESSION", "Jobbe"),
	)
	action = models.CharField(choices=ACTION_CHOICES, max_length=10)
	started = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	ended = models.DateTimeField(blank=True, null=True)
	slave = models.ForeignKey('slave.Slave', related_name='actions')

	def is_break(self):
		return self.action == "BREAK"

	def is_session(self):
		return self.action == "SESSION"

	def end(self):
		self.ended = timezone.localtime(timezone.now())
		self.save()

	def is_active(self):
		return self.ended != None

class FeedItem(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	slave = models.ForeignKey('slave.Slave', related_name='feed')
	desc = models.CharField(max_length=100)

	def __unicode__(self):
		return self.desc

