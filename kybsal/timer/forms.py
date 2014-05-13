from django import forms
from .models import FeedItem

class CreateFeedItemForm(forms.ModelForm):
	class Meta:
		model = FeedItem
		fields = ['desc']

	def is_valid(self):
		valid = super(CreateFeedItemForm, self).is_valid()
		if not valid:
			return False
		if len(self.cleaned_data.get('desc')) <= 0:
			return False
		return True

	def save(self, slave, *args, **kwargs):
		kwargs['commit'] = False
		feeditem = super(CreateFeedItemForm, self).save(*args, **kwargs)
		feeditem.desc = "%s: %s" % (slave.get_full_name(), feeditem.desc)
		feeditem.slave = slave
		feeditem.save()
		return feeditem