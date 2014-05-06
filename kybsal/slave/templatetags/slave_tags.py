from django import template
from kybsal.slave.models import Slave
register = template.Library()

@register.inclusion_tag('dashboard.jade', takes_context = True)
def show_slave_dashboard(context):
	return {'user': context['user']}