from django import template

register = template.Library()

@register.inclusion_tag('list_activities.jade', takes_context = True)
def list_activities(context, activities):
	return {'user': context['user'], 'activities': activities}