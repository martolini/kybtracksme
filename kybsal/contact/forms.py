from django.forms import forms, widgets
from django.forms.models import ModelForm
from kybsal.contact.models import Improvement

class ImprovementForm(ModelForm):
	class Meta:
		model = Improvement
		exclude = ('solved',)
		widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Hva gjelder det?'},),
            'abstract': forms.Textarea(attrs={'rows': '4'},),
            'sender': widgets.HiddenInput(),
        }
