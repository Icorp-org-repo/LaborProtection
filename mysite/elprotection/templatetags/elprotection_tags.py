from django import template
from django.db.models import Count
from ..models import Protocol

register = template.Library()


@register.inclusion_tag('elprotection/intags/sidebar.html')
def show_sidebar():
    return {}
