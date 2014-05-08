from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from kybsal.contact.models import Improvement

class ImprovementAdmin(ModelAdmin):
	list_display = ('title', 'sender', 'date', 'solved')
	list_filter = ('solved',)

admin.site.register(Improvement, ImprovementAdmin)
