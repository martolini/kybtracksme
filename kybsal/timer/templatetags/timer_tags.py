from django import template

register = template.Library()

@register.inclusion_tag('list_activities.jade', takes_context = True)
def list_activities(context, feed):
	return {'user': context['user'], 'feed': feed}