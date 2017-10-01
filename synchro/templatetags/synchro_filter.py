from django import template                                                                 
from django.template.defaultfilters import stringfilter
from ..models import *
register = template.Library()

@register.filter
def activity_user_relation(activity, user):
	return activity.userTag(user)

@register.filter
@stringfilter
def oversimple(s):
	return s+" [did something]"

@register.filter
@stringfilter
def get_all(s):
	s = s.lower()
	if(s=="slots"):
		return Slot.objects.all()
	return None

@register.filter('not')
def not_filter(b):
	return not(b)

@register.filter('print')
def print_filter(value):
	print(value.field.widget.__dict__)
	return ""
