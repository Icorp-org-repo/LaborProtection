from django import template
from django.db.models import Count
from ..models import Protocol

register = template.Library()

@register.inclusion_tag('elprotection/include/sidebar.html')
def show_categories(sort=None):

    return {"cats": cats, 'cat_selected': cat_selected}
