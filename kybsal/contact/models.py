from django.db import models
from django.utils.translation import ugettext_lazy as _

class Improvement(models.Model):
	title = models.CharField(max_length=50, verbose_name=_('Tittel'))
	sender = models.CharField(max_length=50, verbose_name=_('Avsender'))
	abstract = models.TextField(verbose_name=_('Beskjed'))
	date = models.DateTimeField(auto_now_add=True)
	solved = models.BooleanField(default=False, verbose_name=_('Solved'))

	def __unicode__(self):
		return self.title

