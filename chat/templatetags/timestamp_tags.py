import datetime
# Otherwise use timezone
from django.utils import timezone

from django import template

register = template.Library()

@register.filter
def hours_ago(time, hours=1):
    return time + datetime.timedelta(hours=hours) > timezone.now() # or timezone.now()

@register.filter
def weeks_ago(time, weeks=1):
    return time + datetime.timedelta(weeks=weeks) > timezone.now()

