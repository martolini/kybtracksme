from django.contrib import admin
from .models import Slave
from .forms import SlaveChangeForm

class SlaveAdmin(admin.ModelAdmin):
	model = Slave
	form = SlaveChangeForm
	list_display = ('username', 'first_name', 'last_name')

	def get_todays_hours(self, obj):
		return obj.get_total_hours_from_workday(obj.get_today_workday())

admin.site.register(Slave, SlaveAdmin)
