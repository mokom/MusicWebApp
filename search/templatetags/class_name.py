from django import template

register = template.Library()

@register.filter()
def class_name(value):
    return value.__class__.__name__ # returns the name of any given class