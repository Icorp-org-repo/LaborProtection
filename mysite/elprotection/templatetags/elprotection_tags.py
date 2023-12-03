from django import template
from django.db.models import Count
from ..models import Protocol

register = template.Library()


@register.inclusion_tag('elprotection/intags/sidebar.html')
def show_sidebar( active_item=None, ):
    return {'list_menu':
            [
                {'title': "Личный кабинет", 'url': 'elprotection:employ',},
                {'title': 'Журнал', 'url': 'elprotection:protocols',},
                {'title': 'Сотрудники', 'url': 'elprotection:list_employ', }
            ],
            'active_item': active_item}

