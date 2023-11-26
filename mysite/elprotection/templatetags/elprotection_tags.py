from django import template
from django.db.models import Count
from ..models import Protocol

register = template.Library()


@register.inclusion_tag('elprotection/intags/sidebar.html')
def show_sidebar(active_item=None):
    return {'list_menu':
                [{'title': 'Журнал', 'url': 'elprotection:protocols',},
                 {'title': 'Предприятии', 'url': 'elprotection:list_company',}],
            'active_item': active_item}

