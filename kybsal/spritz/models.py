from django.db import models

class KapittelManager(models.Manager):
	def get_queryset(self):
		return super(KapittelManager, self).get_queryset().order_by('nummer')

class Kapittel(models.Model):
	tittel = models.CharField(max_length=100, blank=True, null=True)
	nummer = models.PositiveIntegerField(blank=True, null=True)
	text = models.TextField(blank=True, null=True)
	objects = KapittelManager()

	def __unicode__(self):
		return "Kapittel %d: %s" % (self.nummer, self.tittel)
