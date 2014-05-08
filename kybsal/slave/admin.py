from django.contrib import admin
from .models import Slave

class SlaveAdmin(admin.ModelAdmin):
	model = Slave
	list_display = ('username', 'first_name', 'last_name','get_total_hours', 'get_todays_hours', 'has_active_workday')

	def get_todays_hours(self, obj):
		return obj.get_total_hours_from_workday(obj.get_today_workday())

	def has_active_workday(self, obj):
		return len(obj.workdays.filter(active=True)) > 0
	has_active_workday.boolean = True
	has_active_workday.short_description = "Checked in"


admin.site.register(Slave, SlaveAdmin)
