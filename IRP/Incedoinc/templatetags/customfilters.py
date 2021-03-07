from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

@register.filter
@stringfilter
def custom_lower(value):
    return value.lower()

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)

# @register.filter
# @stringfilter
# def get