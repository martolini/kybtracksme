from django import template
from kybsal.slave.models import Slave
from django.utils import timezone
from datetime import timedelta
register = template.Library()

@register.inclusion_tag('dashboard.jade', takes_context = True)
def show_slave_dashboard(context):
	slave = context['user']
	if not slave.is_anonymous():
		effektive_timer, totale_timer_idag, totale_timer_idag = 0, 0, 0
		now = timezone.localtime(timezone.now())
		since = now-timedelta(hours=now.hour)
		queryset = slave.actions.filter(started__gte=since)
		return {
					'user': context['user'],
					'effektive_timer': slave.get_effective_hours(queryset),
					'totale_timer_idag': slave.get_total_hours(queryset), 
					'totale_timer': slave.get_total_hours(slave.actions.all())
				}
	else:
		return {'user': slave}