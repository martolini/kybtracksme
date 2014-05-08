from django import template
from kybsal.slave.models import Slave
register = template.Library()

@register.inclusion_tag('dashboard.jade', takes_context = True)
def show_slave_dashboard(context):
	slave = context['user']
	if not slave.is_anonymous():
		workday = slave.get_today_workday()
		effektive_timer = slave.get_effective_hours_from_workday(workday)
		totale_timer_idag = slave.get_total_hours_from_workday(workday)
		totale_timer = slave.get_total_hours()
		return {
					'user': context['user'],
					'effektive_timer': effektive_timer,
					'totale_timer_idag': totale_timer_idag, 
					'totale_timer': totale_timer
				}
	else:
		return {'user': slave}