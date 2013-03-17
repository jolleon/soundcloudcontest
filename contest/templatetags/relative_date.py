from django import template
from django.utils.dateformat import format
from time import mktime, localtime

register = template.Library()

def create_time_string(seconds):
    hours = seconds / 3600
    minutes = (seconds % 3600) / 60
    days = hours/24
    weeks = days/7
    months = days/30
    years = months/12

    if years > 0:
        if years > 1:
            return "" + str(years) + " years"
        return "1 year"
    if months > 0:
        if months > 1:
            return "" + str(months) + " months"
        return "1 month"
    if weeks > 0:
        if weeks > 1:
            return str(weeks) + " weeks"
        return "1 week"
    if days > 0:
        if days > 1:
            return str(days) + " days"
        return "1 day"
    if hours > 0:
        if hours > 1:
            return str(hours) + " hours"
        return "1 hour"
    if minutes > 0:
        if minutes > 1:
            return str(minutes) + " minutes"
        return "1 minute"

    return "moments"

@register.filter
def relative_date(value):
    then = int(format(value, 'U'))
    now = int(mktime(localtime()))

    return create_time_string(now - then)
