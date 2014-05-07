from django.contrib import admin
from .models import Slave

class SlaveAdmin(admin.ModelAdmin):
	model = Slave
	list_display = ('username', 'first_name', 'last_name', 'get_todays_effective_hours', 'get_todays_total_hours' ,'get_total_hours')

admin.site.register(Slave, SlaveAdmin)
