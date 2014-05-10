from django.contrib import admin
from .models import *

class WorkdayAdmin(admin.ModelAdmin):
	model = Workday
	list_display = ('slave', 'date', 'checked_in', 'checked_out')

class BreakAdmin(admin.ModelAdmin):
	model = Break
	list_display = ('get_slave', 'workday', 'started', 'ended')

	def get_slave(self, obj):
		return obj.workday.slave

	def get_date(self, obj):
		return obj.workday.date

	get_date.short_description = "Date"

	get_slave.short_description = "Slave"

class SessionAdmin(admin.ModelAdmin):
	model = Session
	list_display = ('get_slave', 'workday', 'started', 'ended')

	def get_slave(self, obj):
		return obj.workday.slave

	def get_date(self, obj):
		return obj.workday.date

	get_date.short_description = "Date"

	get_slave.short_description = "Slave"

class ActionAdmin(admin.ModelAdmin):
	model = Action
	list_display = ('slave', 'action', 'started', 'ended')
	search_fields = ('slave__username', 'slave__first_name', 'slave__last_name')

class FeedItemAdmin(admin.ModelAdmin):
	model = FeedItem
	list_display = ('desc', 'created')
	search_fields = ('slave__username', 'slave__first_name', 'slave__last_name')

admin.site.register(Break, BreakAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Workday, WorkdayAdmin)
admin.site.register(Activity)
admin.site.register(Action, ActionAdmin)
admin.site.register(FeedItem, FeedItemAdmin)