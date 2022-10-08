from atexit import register
from django import template
from users_data.models import WatchList
register= template.Library()
@register.filter(name='subscribersinthousand')
def subscribersinthousand(number):
    if int(number) >=1000:
        new_number= int(number)/1000
        new_number = str(new_number) + 'K'
        return new_number
    else:
        return number